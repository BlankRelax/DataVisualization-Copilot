import abc

class BaseSupersetObject(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def create(self):
        return
    
    @abc.abstractmethod
    def delete(self):
        return
    
    @abc.abstractmethod
    def _update_info_all(self):
        return
    
    @abc.abstractmethod
    def _update_info(self):
        return
    
    @abc.abstractmethod
    def info_all(self):
        return
    
    @abc.abstractmethod
    def info(self):
        return
    
    