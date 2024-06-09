import pandas as pd
class File:
    def __init__(self,name,path) -> None:
        self.fileName=name
        self.filePath=path
    
    def getFilePath(self):
        return self.filePath
    
    def __str__(self) -> str:
        return f"The File: '{self.fileName}' at path '{self.filePath}'"
    
class CSV(File):
    def __init__(self, name, path) -> None:
        super().__init__(name, path)

    def readCsv(self):
        dataFrame=pd.read_csv(self.getFilePath())
        return dataFrame
    
    def getCsvSample(self,numberOfSamples=5):
        dataFrame=self.readCsv()
        return dataFrame.head(numberOfSamples)