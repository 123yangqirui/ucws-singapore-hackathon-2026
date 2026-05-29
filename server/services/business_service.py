import json
import sys
from typing import List, Optional, Dict, Any

from schemas import (
    CompanyBasicInfoRequest,
    CompanyBasicInfoResponse,
    ApprovalInfoRequest,
    ApprovalInfoResponse,
    EmployeeCountRequest,
    EmployeeCountResponse,
    BusinessScopeRequest,
    BusinessScopeResponse,
    CapitalRequest,
    CapitalResponse,
    AddressRequest,
    AddressResponse,
)
from .llm_service import llm_service


class BusinessService:
    """业务逻辑服务 - 统一返回标准格式: {code, status, message, data}"""
    
    @staticmethod
    async def process_page1_generate_names(request: CompanyBasicInfoRequest) -> dict[
        str, int | str | CompanyBasicInfoResponse]:
        """
        第一页：处理公司基本信息
        - 输入：公司名称、描述信息
        - 生成公司名称建议
        """
        # 构建一组提示词：系统提示词、用户提示词、综合消息
        system_prompt = """你是一位专业的公司注册顾问。
        Please parse the "names" and output them in JSON format.
        EXAMPLE JSON OUTPUT:
        {
            "names": ["星禾云创科技有限公司", "星禾云创商务有限公司", "星禾云创网络有限公司"]
        }
        """
        prompt = f"""
                请根据用户的输入参考名称和描述信息作为参考。
                生成3-5个公司包含用户偏好词的名称设计，用户偏好词可以在名称的任意位置，生成的名称要符合中国大陆的公司命名规范，且尽量体现业务特点，不要过于通用。
                用户偏好词：[{request.namePref}]
                用户的业务描述：{request.desc}
                """
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]

        try:
            response = await llm_service.chat(messages=messages, temperature=0.0)
            data = json.loads(response)

            return {
                "code": 200,
                "status": "success",
                "message": "生成公司名称成功",
                "data": CompanyBasicInfoResponse(names=data.get("names", []))
            }
        except Exception as e:
            # 返回默认响应
             return {
                "code": 500,
                "status": "error",
                "message": f"生成公司名称失败: {str(e)}",
                "data": CompanyBasicInfoResponse(
                    names=["名称一", "名称二", "名称三", "名称四", "名称五"]
                )
            }
    
    @staticmethod
    async def process_page2_check_approval(request: ApprovalInfoRequest) -> dict[str, int | str | ApprovalInfoResponse]:
        """
        第二页：审批信息
        - 输入：主要经营范围,具体描述
        - 输出：是否需要审批、审批类型、审批详情
        """
        # 构建一组提示词：系统提示词、用户提示词、综合消息
        system_prompt = """你是一位专业的公司注册顾问。
        Please parse the "needsApproval" and "type" and "detail" and output them in JSON format.
        EXAMPLE JSON OUTPUT:
        {
            "needsApproval": true,#这个返回的是布尔值
            "type": "前置审批",# 从["前置审批","后置审批",""] 中选择,不需要审批选择空字符串
            "details": "公司需要在注册前获得相关审批，才能正式注册。"
        }
        """
        prompt = f"""
                请根据用户的输入行业大类和具体描述(可选)，判断是否需要审批、审批类型、审批详情。如果需要审批，请给出对应的规则。
                行业大类：{request.industry}
                具体描述：{request.desc}(可选)
                """
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]

        try:
            response = await llm_service.chat(messages=messages, temperature=0.0)
            data = json.loads(response)
            return {
                "code": 200,
                "status": "success",
                "message": "查询审批信息成功",
                "data": ApprovalInfoResponse(
                    needsApproval=data.get("needsApproval"),
                    type=data.get("type"),
                    details=data.get("details"),
                )
            }
        except Exception as e:
            return {
                "code": 500,
                "status": "error",
                "message": f"查询审批信息失败: {str(e)}",
                "data": ApprovalInfoResponse(
                    needsApproval=True,
                    type="后置审批",
                    details="建筑施工及相关业务需在工商登记后取得资质证书方可承接工程。\n\n• 建筑施工：建筑业企业资质证书（住房和城乡建设部门）\n• 工程设计：工程设计资质证书\n• 工程监理企业资质证书\n\n资质申请需满足注册资本、技术人员、业绩等要求，办理时限约60个工作日",
                )
            }
    @staticmethod
    async def process_page3_business_scope(request: BusinessScopeRequest) -> dict[
        str, int | str | BusinessScopeResponse]:
        """
        第三页：生成经营范围
        - 一个formData结构，包含多个字段
        - 输出：主营业务，其他经营范围项目
        """
        system_prompt = """你是一位专业的公司注册顾问。
        Please parse the "main" and "others" and output them in JSON format.
        EXAMPLE INPUT: 
        主营业务类型：(I) 信息传输、软件和信息技术服务业
        人数：10
        股东数量：3
        公司名称偏好：星河云创
        最终公司名称：星禾云创科技有限公司
        EXAMPLE JSON OUTPUT:
        {
            "main": "软件开发",
            "others": ["信息系统集成服务", "技术服务", "技术咨询", "数据处理服务"]
        }
        """
        prompt = f"""
        请根据用户的输入信息作为参考，生成3-5个相关的其他经营范围项目：
        主营业务类型：{request.formData.business}
        人数：{request.formData.people}
        股东数量：{request.formData.shareholder}
        公司名称偏好：{request.formData.namePref}
        最终公司名称：{request.formData.name}
        """ 
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        
        try:
            response = await llm_service.chat(messages=messages, temperature=0.0)
            data = json.loads(response)
            return {
                "code": 200,
                "status": "success",
                "message": "生成经营范围成功",
                "data": BusinessScopeResponse(
                    main=data.get("main"),
                    others=data.get("others")
                )
            }
        except Exception as e:
            return {
                "code": 500,
                "message": f"生成经营范围失败: {str(e)}",
                "status": "error",
                "data": BusinessScopeResponse(
                    main=request.formData.business,
                    others=["错误信息", "错误信息", "错误信息"]
                )
            }


    @staticmethod
    async def process_page4_company_type(request: EmployeeCountRequest) -> dict[str, int | str | EmployeeCountResponse]:
        """
        第四页：根据基础信息推荐公司类型
        输入：公司人数、股东人数、前面已填写信息
        输出：推荐公司类型、解释说明原因
        """
        system_prompt = """你是一位专业的公司注册顾问。
        Please parse the "companyType" and "explanation" and output them in JSON format.

        EXAMPLE JSON OUTPUT:
        {
            "companyType": "有限责任公司",
            "explanation": "这里是为什么选择'有限责任公司'的说明。"
        }
        """
        prompt = f"""
        请根据用户的输入信息作为参考，推荐公司类型以及解释说明原因：
        公司人数：{request.people}
        股东人数：{request.shareholder}
        主营业务类型：{request.formData.business}
        行业：{request.formData.business}
        名称偏好：{request.formData.namePref}
        最终公司名称：{request.formData.name}
        主营业务：{request.formData.scope.main}
        其他经营范围：{request.formData.scope.others}
        """ 
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        
        try:
            response = await llm_service.chat(messages=messages, temperature=0.0)
            data = json.loads(response)
            return {
                "code": 200,
                "status": "success",
                "message": "推荐公司类型成功",
                "data": EmployeeCountResponse(
                    companyType=data.get("companyType"),
                    explanation=data.get("explanation")
                )
            }
        except Exception as e:
            return {
                "code": 500,
                "status": "error",
                "message": f"推荐公司类型失败: {str(e)}",
                "data": EmployeeCountResponse(
                    companyType="",
                    explanation="错误信息"
                )
            }
    
    
    @staticmethod
    async def process_page5_capital_estimate(request: CapitalRequest) -> dict[str, int | str | CapitalResponse]:
        """
        第五页：预估注册资本
        - 输入：意向金额(万元)、前面已填写信息
        - 输出：预估金额(万元)
        """
        system_prompt = """你是一位专业的公司注册顾问。
        Please parse the "estimated_amount" and output them in JSON format.
        EXAMPLE JSON OUTPUT:
        {
            "estimatedAmount": 预估金额(万元)
        }
"""
        prompt = f"""
        请根据用户输入信息作为参考，综合分析结合公司创办过程、可能会遇到的风险等等因素综合推理生成预估注册资本（万元）
        意向注册资本：{request.capitalIntention}（万元）
        主营业务类型：{request.formData.business}
        人数：{request.formData.people}
        股东数量：{request.formData.shareholder}
        公司类型：{request.formData.companyType}
        公司名称偏好：{request.formData.namePref}
        最终公司名称：{request.formData.name}
        主营业务：{request.formData.scope.main}
        其他经营范围：{request.formData.scope.others}
        """

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        
        try:
            response = await llm_service.chat(messages=messages, temperature=0.0)
            data = json.loads(response)
            return {
                "code": 200,
                "status": "success",
                "message": "预估注册资本成功",
                "data": CapitalResponse(
                    estimatedAmount=float(data.get("estimatedAmount", request.capitalIntention))
                )
            }
        except Exception as e:
            return {
                "code": 500,
                "status": "error",
                "message": f"预估注册资本失败: {str(e)}",
                "data": CapitalResponse(
                    estimatedAmount=request.capitalIntention,
                )
            }
    
    @staticmethod
    async def process_page6_address_recommend(request: AddressRequest) -> dict[str, int | str | AddressResponse]:
        """
        第六页：推荐注册地址类型
        根据主营业务、注册资本和省份推荐
        """
        system_prompt = """你是一位专业的公司注册顾问。
        Please parse the "province" and "recommendation" and "explanation" and output them in JSON format.
        EXAMPLE JSON OUTPUT:
        {
            "recommendation": "商用办公地址",#从这四个种类中选取（商用办公地址、园区/孵化器地址、虚拟地址、住宅地址）
            "explanation": "推荐理由"#详细说明不要过于简短
        }

"""
        prompt = f"""
            请根据用户的输入的信息作为参考，推荐注册地址类型以及解释说明原因：
            省份：{request.province}
            主营业务类型：{request.formData.business}
            人数：{request.formData.people}
            股东数量：{request.formData.shareholder}
            公司名称偏好：{request.formData.namePref}
            最终公司名称：{request.formData.name}
            主营业务：{request.formData.scope.main}
            其他经营范围：{request.formData.scope.others}
            意向注册资本：{request.formData.capital}（万元）

            推理生成推荐的地址类型和推荐理由
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        
        try:
            response = await llm_service.chat(messages=messages, temperature=0.0)
            data = json.loads(response)
            return {
                "code": 200,
                "status": "success",
                "message": "推荐注册地址成功",
                "data": AddressResponse(
                    province=request.province,
                    recommendation=data.get("recommendation", ""),
                    explanation=data.get("explanation", "")
                )
            }
        except Exception as e:
            return {
                "code": 500,
                "status": "error",
                "message": f"推荐注册地址失败: {str(e)}",
                "data": AddressResponse(
                    province=request.province,
                    recommendation="",
                    explanation=""
                )
            }
