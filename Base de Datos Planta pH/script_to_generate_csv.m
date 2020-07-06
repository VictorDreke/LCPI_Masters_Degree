
[labelXall,labelXall_cell,DataSetH,DataSetPH,InDNormH,InDNormPH,Cat_pH]=dataSetMaker2("DGR",'C',true);
[labelXall,labelXall_cell,DataSet,InDNorm,Cat]=dataSetMakerClarke("C",true);

DataSet_Final = [DataSet array2table(Cat,'VariableNames',{'Category'})];
DataSetH_Final = [DataSetH array2table(Cat_pH(:,1),'VariableNames',{'Category'})];
DataSetPH_Final = [DataSetPH array2table(Cat_pH(:,2),'VariableNames',{'Category'})];

Model_Number_Table = array2table([1:3150]', 'VariableNames', {'Model_No'});
Model_Number_Table2 = array2table([1:5250]', 'VariableNames', {'Model_No'});

writetable([Model_Number_Table2 DataSet_Final],'Clarke_DataSet.txt');
writetable([Model_Number_Table DataSetH_Final],'Neutralization_DataSet_H.txt');
writetable([Model_Number_Table DataSetPH_Final],'Neutralization_DataSet_pH.txt');
