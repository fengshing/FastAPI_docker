# 1203新增 用來宣告如何讀寫表格資料的文件
from fastapi import HTTPException, status
from sqlalchemy.orm.session import Session
from .models import DbWorklist 
from .OneTableWorkList import WorkList
#ast，一種py的內建模塊。這在處理從資料庫或其他來源獲取的數據時非常有用，特別是當這些數據以非標準格式存儲時。例如，將字符串形式的列表 "[1, 2, 3]" 轉換為真正的列表 [1, 2, 3]。
import ast
#有了schemas後，導入使用做資料響應
from router.schemas import WorkListResponseSchema, WorkListRequestSchema


# 以下的值與命名邏輯需要參照database.py以及models.py才行。

# 初始化資料庫。從預先定義的資料集合（OneTableWorkList中的WorkList）中讀取資料，並將這些資料寫入到DbWorklist模型對應的資料庫表中。先清空表中現有資料，再添加新資料。
def db_feed(db: Session):
    new_workList_list = [DbWorklist(
        school=worklist["school"],
        semester=worklist["semester"],
        workName=worklist["workName"],
        githubUrl=worklist["githubUrl"],
        websiteUrl=worklist["websiteUrl"],
        pptUrl=worklist["pptUrl"],
        imgUrl=worklist["imgUrl"],
        skill=worklist["skill"],
        name=worklist["name"]
    ) for worklist in WorkList]
    db.query(DbWorklist).delete()
    db.commit()
    db.add_all(new_workList_list)
    db.commit()
    db_items = db.query(DbWorklist).all()
    return [WorkListResponseSchema.from_orm(item) for item in db_items] #套入schemas響應，每個項目都做感應與響應

def create(db: Session, request: WorkListRequestSchema):
    new_worklist = DbWorklist(
        school=request.school,
        semester=request.semester,
        workName=request.workName,
        githubUrl=request.githubUrl,
        websiteUrl=request.websiteUrl,
        pptUrl=request.pptUrl,
        imgUrl=request.imgUrl,
        skill=request.skill,
        name=request.name
    )
    db.add(new_worklist)
    db.commit()
    db.refresh(new_worklist)
    return WorkListResponseSchema.from_orm(new_worklist)

# 從資料庫中檢索所有DbWorklist記錄。如果沒有找到任何記錄，則引發HTTP 404錯誤。
def get_all(db: Session):
    worklist = db.query(DbWorklist).all()
    if not worklist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'worklist not found')
    return [WorkListResponseSchema.from_orm(item) for item in worklist]

# 從資料庫中讀取特定學期的worklist記錄。如果沒有找到符合指定學期的紀錄，會引發HTTP 404異常，否則返回這些紀錄。
def get_worklist_by_semester(semester: str, db: Session):
    #從資料庫中查詢所有學期等於（==）指定semester值的worklist記錄。
    worklist = db.query(DbWorklist).filter(DbWorklist.semester == semester).all()
    if not worklist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'worklist with semester = {semester} not found')
    return [WorkListResponseSchema.from_orm(item) for item in worklist]

# 從資料庫中讀取特定學校的worklist記錄。如果沒有找到符合指定學校的紀錄，會引發HTTP 404異常，否則返回這些紀錄。
def get_worklist_by_school(school: str, db: Session):
    #從資料庫中查詢所有學校等於（==）指定school值的worklist記錄。
    worklist = db.query(DbWorklist).filter(DbWorklist.school == school).all()
    if not worklist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'worklist with school = {school} not found')
    return [WorkListResponseSchema.from_orm(item) for item in worklist]

# 優化UX，製作一個先學校後學期的模式；先保留，自創代碼不確定用不用得上
#def get_worklist_by_school_and_semester(school: str, semester: str, db: Session):
#    worklist = db.query(DbWorklist).filter(DbWorklist.school == school, DbWorklist.semester == semester).all()
#    if not worklist:
#        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                            detail=f'worklist for school {school} and semester {semester} not found')
#    return [WorkListResponseSchema.from_orm(item) for item in worklist]


# 優化資料空值的處理，還有將資料轉換成列表；先保留，老師代碼裡刪掉了
def str2List(worklist_records: list):
    for record in worklist_records:
        if record.skill:  
            record.skill = ast.literal_eval(record.skill)
        if record.name:  
            record.name = ast.literal_eval(record.name)
    return worklist_records

# 從資料庫中讀取特定id的worklist記錄。如果沒有找到符合指定id的紀錄，會引發HTTP 404異常，否則返回這些紀錄。 
def get_worklist_by_id(id: int, db: Session):
    # first() 方法則從查詢結果中返回第一個匹配的記錄，或在沒有匹配時返回 None。
    homework = db.query(DbWorklist).filter(DbWorklist.id == id).first()
    if not homework:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Homework with id = {id} not found')
    return WorkListResponseSchema.from_orm(homework)