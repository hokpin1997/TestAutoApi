# -*- coding:utf-8 -*-
from typing import Text, Dict, Callable, Union, Optional, List, Any
from pydantic import BaseModel, Field


class ResponseData(BaseModel):
    url: Text
    is_dependence_login: Union[None, bool, Text]
    detail: Text
    request_body: Any
    response_text: Any
    response_json: Any
    method: Text
    yaml_data: Any
    headers: Dict
    cookie: Dict
    assert_data: Any
    res_time: Union[int, float]
    status_code: int


class Config(BaseModel):
    host: Text
    ws_host: Text
    mysql_db: Dict
