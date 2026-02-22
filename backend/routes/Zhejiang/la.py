import os
import tempfile
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from fastapi.background import BackgroundTasks
from typing import Dict, Any

# 引入生成逻辑
from WenShu.Zhejiang.LAdocx import generate_LAdocx

router = APIRouter()

# 定义清理临时文件的任务
def remove_file(path: str):
    try:
        os.remove(path)
    except Exception:
        pass

@router.post("/generate")
async def generate_zj_la(req: Dict[str, Any], background_tasks: BackgroundTasks):
    """
    浙江省劳动仲裁申请书生成接口
    """
    try:
        # 1. 获取前端数据 (Vue 发送的是 JSON 字典)
        data = req

        # 辅助函数：安全获取 Vue 发来的驼峰字段，如果没填则返回空字符串
        def get(key, default=''):
            return str(data.get(key, default)).strip()

        # 2. 处理日期范围数组
        all_date_ranges = data.get('all_date_ranges', [])
        if not isinstance(all_date_ranges, list):
            all_date_ranges = []

        # 3. 数据映射与调用
        # 核心修改：将 Vue 的 "applicantName" 映射给函数的 "claimant"
        # 使用关键字参数 (key=value) 调用，确保数据准确填入
        
        doc = generate_LAdocx(
            # --- 申请人信息 ---
            claimant=get('applicantName'),           # Vue: applicantName
            gender=get('gender'),                    # Vue: gender
            birthday_year=get('birthYear'),          # Vue: birthYear
            birthday_month=get('birthMonth'),
            birthday_day=get('birthDay'),
            phone_claimant=get('phone'),             # Vue: phone
            id_number=get('idNumber'),               # Vue: idNumber
            nationality=get('nationality', '汉'),    # Vue 没有这个字段，暂时默认
            occupation=get('jobPosition'),           # Vue: jobPosition (映射为职业)
            registered_address=get('address'),       # Vue: address (暂时共用)
            residence_address=get('address'),        # Vue: address
            
            # --- 被申请人信息 ---
            respondent=get('respondentName'),             # Vue: respondentName
            legal_representative=get('legalRepName'),     # Vue: legalRepName
            phone_respondent=get('legalRepContact'),      # Vue: legalRepContact
            respondent_address=get('respondentAddress'),  # Vue: respondentAddress
            social_unity_credit_code=get('socialCreditCode', ''), # Vue 暂时没这个字段
            
            # --- 核心诉求 ---
            recourse_amount=get('recourseAmount', '______'), # 追索总金额
            
            # --- 欠薪时间段 1 (Pre) ---
            # 如果 Vue 还没做这些日期的输入框，这里会是空字符串，文档里会留空
            debt_year_pre=get('debtYearStart'),   
            debt_month_pre=get('debtMonthStart'), 
            debt_day_pre=get('debtDayStart'), 
            
            # --- 欠薪时间段 2 (Sub/End) ---
            debt_year_sub=get('debtYearEnd'),
            debt_month_sub=get('debtMonthEnd'), 
            debt_day_sub=get('debtDayEnd'), 
            
            # --- 入职时间 ---
            hiredate_year=get('hireYear'),       # Vue: hireYear
            hiredate_month=get('hireMonth'),     # Vue: hireMonth
            hiredate_day=get('hireDay'),         # Vue: hireDay
            
            # --- 工资标准 ---
            monthly_salary_standard=get('monthlySalary', ''), # Vue 需添加此字段
            
            # --- 未支付时间段 (LAdocx定义了重复的字段，这里再次映射) ---
            unpaid_year_pre=get('debtYearStart'),
            unpaid_month_pre=get('debtMonthStart'),
            unpaid_day_pre=get('debtDayStart'),
            unpaid_year_sub=get('debtYearEnd'),
            unpaid_month_sub=get('debtMonthEnd'),
            unpaid_day_sub=get('debtDayEnd'),
            
            # --- 其他 ---
            respondent_city=get('submitCity', '______'),  # Vue: submitCity
            all_date_ranges=all_date_ranges
        )

        # 4. 保存为临时文件
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
            doc.save(tmp.name)
            tmp_path = tmp.name

        # 5. 设置后台任务删除临时文件
        background_tasks.add_task(remove_file, tmp_path)

        # 6. 生成文件名
        name = get('applicantName') or "申请人"
        filename = f"{name}的追索劳动报酬仲裁申请书.docx"
        
        # 7. 返回文件
        return FileResponse(
            tmp_path, 
            filename=filename,
            media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )

    except Exception as e:
        print(f"Error generating ZJ LA: {e}")
        raise HTTPException(status_code=500, detail=str(e))