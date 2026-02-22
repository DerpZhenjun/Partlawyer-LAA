import os
import tempfile
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from fastapi.background import BackgroundTasks
from typing import Dict, Any

# 引入生成逻辑
from WenShu.Guangdong.LAdocx import generate_LAdocx

router = APIRouter()

def remove_file(path: str):
    try:
        os.remove(path)
    except Exception:
        pass

@router.post("/generate")
async def generate_gd_la(req: Dict[str, Any], background_tasks: BackgroundTasks):
    try:
        # 1. 提取数据
        data = req
        def get(key):
            return str(data.get(key, '')).strip()

        # 2. 准备 additionalFacts
        raw_facts = data.get('additionalFacts')
        additional_facts = []
        if isinstance(raw_facts, str) and raw_facts.strip():
            additional_facts = [raw_facts.strip()]
        elif isinstance(raw_facts, list):
            additional_facts = raw_facts

        # 3. 定位 Word 模板路径
        # 当前文件: .../backend/routes/Guangdong/la.py
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # 回退两层，到达 backend 目录
        # level 1: .../backend/routes
        # level 2: .../backend
        backend_dir = os.path.dirname(os.path.dirname(current_dir)) 
        
        # 拼接目标路径: .../backend/templates_docx/Guangdong/仲裁申请书.docx
        template_path = os.path.join(
            backend_dir, 
            'templates_docx', 
            'Guangdong', 
            '仲裁申请书.docx'
        )

        # 4. 再次检查
        if not os.path.exists(template_path):
            print(f"【严重错误】依然找不到文件: {template_path}")
            fallback_path = r"D:\workspace\PartLawyer\backend\templates_docx\Guangdong\仲裁申请书.docx"
            if os.path.exists(fallback_path):
                print(">>> 使用硬编码路径作为备选方案")
                template_path = fallback_path
            else:
                raise HTTPException(status_code=500, detail=f"模板彻底丢失，请检查: {template_path}")

        # 5. 准备调用参数
        call_params = {
            "submitCity": get('submitCity'),
            "applicantName": get('applicantName'),
            "gender": get('gender'),
            "birthYear": get('birthYear'),
            "birthMonth": get('birthMonth'),
            "birthDay": get('birthDay'),
            "idNumber": get('idNumber'),
            "phone": get('phone'),
            "address": get('address'),
            "addressOption": get('addressOption'),
            "respondentName": get('respondentName'),
            "respondentAddress": get('respondentAddress'),
            "respondentAddressOption": get('respondentAddressOption'),
            "legalRepName": get('legalRepName'),
            "legalRepPosition": get('legalRepPosition'),
            "legalRepContact": get('legalRepContact'),
            
            "arbitrationRequest": data.get('arbitrationRequest', []),
            "requestCalculation": data.get('requestCalculation', []),
            
            "hireYear": get('hireYear'),
            "hireMonth": get('hireMonth'),
            "hireDay": get('hireDay'),
            "jobPosition": get('jobPosition'),
            "contractOption": get('contractOption'),
            "contractStartYear": get('contractStartYear'),
            "contractStartMonth": get('contractStartMonth'),
            "contractStartDay": get('contractStartDay'),
            "contractEndYear": get('contractEndYear'),
            "contractEndMonth": get('contractEndMonth'),
            "contractEndDay": get('contractEndDay'),
            "workLocation": get('workLocation'),
            "workTimeOption": get('workTimeOption'),
            "workDaysPerWeek": get('workDaysPerWeek'),
            "workHoursPerDay": get('workHoursPerDay'),
            "attendanceOption": get('attendanceOption'),
            "attendanceMethod": get('attendanceMethod'),
            
            "salaryOption1": get('salaryOption1'),
            "salaryOption2": get('salaryOption2'),
            "salaryOption3": get('salaryOption3'),
            "salaryOption4": get('salaryOption4'),
            
            "initialSalary": get('initialSalary'),
            "salaryAdjustment": get('salaryAdjustment'),
            "currentEmploymentStatus": get('currentEmploymentStatus'),
            "leaveYear": get('leaveYear'),
            "leaveMonth": get('leaveMonth'),
            "leaveDay": get('leaveDay'),
            "leaveReason": get('leaveReason'),
            "avgMonthlySalary": get('avgMonthlySalary'),
            
            "additionalFact": additional_facts,
            
            "addressAdditionalInput": get('addressAdditionalInput'),
            "respondentAddressAdditionalInput": get('respondentAddressAdditionalInput'),
            "workTimeAdditionalInput": get('workTimeAdditionalInput'),
        }

        # 6. 调用生成函数 (使用 template_docx 参数名)
        doc = generate_LAdocx(**call_params, template_docx=template_path)

        # 7. 保存并返回
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
            doc.save(tmp.name)
            tmp_path = tmp.name

        background_tasks.add_task(remove_file, tmp_path)
        
        filename = f"{get('applicantName')}的仲裁申请书.docx" if get('applicantName') else "仲裁申请书.docx"
        return FileResponse(tmp_path, filename=filename)

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))