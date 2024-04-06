from pydantic import BaseModel, Field
from typing import List, Optional
from bson.objectid import ObjectId

# Union[float, None] = None


class ProjectFields(BaseModel):
    pid: Optional[str] = Field(None)
    created_by: str
    project_name: str
    project_type: str
    project_architecture: str
    project_tags: List[
        str
    ]  # Les tags sont envoyés comme liste de chaînes de caractères


class ProjectOptionalFields(BaseModel):
    project_name: Optional[str] = Field("null")
    project_type: Optional[str] = Field("null")
    project_architecture: Optional[str] = Field("null")
    project_tags: Optional[List[str]] = Field([])


class ProjectAdvancedFields(BaseModel):
    languages: Optional[List[str]] = Field([])
    language_version: Optional[List[str]] = Field([])
    frontend_framework: Optional[str] = Field("null")
    backend_framework: Optional[str] = Field("null")
    add_advanced_configurations: Optional[bool] = Field(False)
    additional_configurations: Optional[List[str]] = Field([])
    authentication_type: Optional[str] = Field("null")
    code_quality_type: Optional[List[str]] = Field([])
    containerization_type: Optional[str] = Field("null")
    testing_type: Optional[List[str]] = Field([])
    package_manager: Optional[str] = Field("null")
    database: Optional[str] = Field("null")


class ProjectInsertFields(ProjectFields, ProjectAdvancedFields):
    pass


class ProjectUpdateFields(ProjectOptionalFields, ProjectAdvancedFields):
    pass


class ProjectReadFields(ProjectFields, ProjectAdvancedFields):
    pass


class ProjectFromFront(BaseModel):
    name: str
    project_type: str
    tags: str  # Les tags sont envoyés sous forme de chaîne de caractères séparés par des virgules
    vcs: Optional[str] = Field("null")
    repo: Optional[str] = Field("null")


class ProjectFromDB(BaseModel):
    _id: ObjectId
    name: str
    project_type: str
    tags: str  # Les tags sont envoyés sous forme de chaîne de caractères séparés par des virgules
    vcs: Optional[str] = Field("null")
    repo: Optional[str] = Field("null")


class ProjectToDB(BaseModel):
    name: str
    project_type: str
    tags: List[str]  # Les tags sont envoyés comme liste de chaînes de caractères
    vcs: Optional[str] = Field("null")
    repo: Optional[str] = Field("null")


class ProjectToFront(BaseModel):
    pid: str
    name: str
    project_type: str
    tags: List[str]  # Les tags sont envoyés comme liste de chaînes de caractères
    vcs: Optional[str] = Field("null")
    repo: Optional[str] = Field("null")
