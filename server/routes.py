from fastapi import APIRouter, HTTPException
from typing import List

#导入格式模板
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

from services import BusinessService

router = APIRouter()

@router.post("/generate-names", response_model=CompanyBasicInfoResponse)
async def page1_generate_names(request: CompanyBasicInfoRequest):
    """
    第一页：公司基本信息
    - 输入：公司名称、主营业务（前端传过来），格式校验后面再完善
    - 输出：3-5个公司名称建议、前置/后置审批判断
    """
    try:
        result = await BusinessService.process_page1_generate_names(request)
        #这里加上返回格式校验
        if result["status"] == "success":
            print("1.公司基本信息，路由返回内容：")
            print(result["data"])
            return result["data"]
        else:
            raise HTTPException(status_code=500, detail=f"处理失败: {result['message']}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理失败: {str(e)}")

@router.post("/check-approval", response_model=ApprovalInfoResponse)
async def page2_check_approval(request: ApprovalInfoRequest):
    """
    第二页：审批信息
    - 输入：业务类型,具体描述
    - 输出：审批信息（是否需要审批、审批类型、审批详情）
    """
    try:
        result = await BusinessService.process_page2_check_approval(request)
        if result["status"] == "success":
            print("2.审批信息，路由返回内容：")
            print(result["data"])
            return result["data"]
        else:
            raise HTTPException(status_code=500, detail=f"处理失败: {result['message']}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理失败: {str(e)}")


@router.post("/business-scope", response_model=BusinessScopeResponse)
async def page3_business_scope(request: BusinessScopeRequest):
    """
    第三页：经营范围
    - 输入：一个formData结构，包含多个字段
    - 输出：多个其他经营范围
    """
    try:
        result = await BusinessService.process_page3_business_scope(request)
        if result["status"] == "success":
            print("3.经营范围，路由返回内容：")
            print(result["data"])
            return result["data"]
        else:
            raise HTTPException(status_code=500, detail=f"处理失败: {result['message']}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理失败: {str(e)}")


@router.post("/company-type", response_model=EmployeeCountResponse)
async def page4_company_type(request: EmployeeCountRequest):
    """
    第四页：根据基础信息推荐公司类型
    输入：公司人数、股东人数、前面已填写信息
    输出：推荐公司类型、解释说明原因
    """
    try:
        result = await BusinessService.process_page4_company_type(request)
        if result["status"] == "success":
            print("4.根据基础信息推荐公司类型，路由返回内容：")
            print(result["data"])
            return result["data"]
        else:
            raise HTTPException(status_code=500, detail=f"处理失败: {result['message']}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理失败: {str(e)}")


@router.post("/capital-estimate", response_model=CapitalResponse)
async def page5_capital_estimate(request: CapitalRequest):
    """
    第五页：注册资本
    - 输入：主营业务类型、注册资本意向金额
    - 输出：预估金额(万元)
    """
    try:
        result = await BusinessService.process_page5_capital_estimate(request)
        if result["status"] == "success":
            print("5.注册资本，路由返回内容：")
            print(result["data"])
            return result["data"]
        else:
            raise HTTPException(status_code=500, detail=f"处理失败: {result['message']}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理失败: {str(e)}")


@router.post("/address-recommendations", response_model=AddressResponse)
async def page6_address_recommend(request: AddressRequest):
    """
    第六页：注册地址
    - 输入：主营业务类型、注册资本、省份
    - 输出：地址类型推荐（商用办公地址、园区/孵化器/集中办公区地址、虚拟地址、住宅地址）
    """
    try:
        result = await BusinessService.process_page6_address_recommend(request)
        if result["status"] == "success":
            print("6.注册地址，路由返回内容：") 
            print(result["data"])
            return result["data"]
        else:
            raise HTTPException(status_code=500, detail=f"处理失败: {result['message']}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理失败: {str(e)}")
