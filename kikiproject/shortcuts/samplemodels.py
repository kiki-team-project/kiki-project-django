class SampleModel:
    HISTORY_COUNT = 10

def get_constants(cls):

    constants = {}
    for attribute_name in dir(cls):
        if attribute_name.isupper():  # 상수는 대문자로 가정합니다.
            value = getattr(cls, attribute_name)
            constants[attribute_name] = value
    return constants

# 클래스 SampleModel에서 상수값 추출
constants = get_constants(SampleModel)