# -*- coding: utf-8 -*-

'''
Created on 2018.03.20�

@author: Administrator
'''

_str_model_name = 'ModelClass'

class MetaClass(type):
    
    def __new__(cls, name, bases, attrs):
        if name == _str_model_name:
            return type.__new__(cls, name, bases, attrs)
        mapping_dic = dict()
        
        for name,value in attrs:
            if isinstance(value , FieldClass):
                mapping_dic[name] = value
            
        for name in mapping_dic.keys():
            attrs.pop(name)   
        
        attrs['sql_mapping'] = mapping_dic
        attrs['sql_table'] = name
        
        return type.__new__(cls, name, bases, attrs)

class ModelClass(dict,metaclass = MetaClass):
    '''
    classdocs
    '''
    
    def __init__(self, **kws):
        '''
        Constructor
        '''
        super(ModelClass,self).__init__(**kws)
    
    def __getattr__(self, key): 
        try:
            return self[key]
        except BaseException:
            return None
     
    def __setattr__(self, key, value):
        self[key] = value
     
    
    def insert(self):
        fields = []
        params = []
        args = []
        for k, v in self.sql_mapping.items():
            fields.append(v.name)
            params.append('?')
            args.append(getattr(self, k, None))
        sql = 'insert into %s (%s) values (%s)' % (self.__table__, ','.join(fields), ','.join(params))
        print('SQL: %s' % sql)
        print('ARGS: %s' % str(args))
    
       
               
class FieldClass(object):
    
    def __init__(self,input_name,input_type):
        self.column_name = input_name
        self.sql_type = input_type
    



       