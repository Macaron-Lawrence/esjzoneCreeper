def apply(src, object):  #obj模板渲染替换
    _f = ''
    # _object = {};
    with open('./modules/templateFiles/' + src, 'r', encoding='utf-8') as f:
        _f = f.read()
        for keys in object.keys():
            _f = _f.replace('{%'+keys+'%}', object[keys])
    return _f