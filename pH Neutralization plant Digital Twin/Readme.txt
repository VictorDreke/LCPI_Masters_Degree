La carpeta se encuentra conformada por las simulaciones de del sistema de control
utilizando el MPC y los modelos originales. En este caso existen simulaciones para 
un MPC que tiene un periodo de muestreo de 60 s (carpeta: MPC con 60s) y simulaciones
para periodo de muestreo de 10 segundos (carpeta: MPC con 60s).

Dentro de cada uno de las carpetas anteriormente mencionadas se encuentran los 
siguientes archivos. Estos son padrones y en cada caso contienen las mismas informaciones
solo dependiendo de los valores de siulaciones propios de su situación:


---------------20200205_SimDataOrigModel.mat------------------------------------

Contiene los datos producto de simular el sistema de control que utiliza los modelos 
para que el MPC prediga los valores de la señal de control.


-----------------20200205_StepInformation.mat-----------------------------------

Contiene los valores de la respuesta temporal del sistmea controlado con los modelos
originales usados por el MPC.En este caso esos valores son calculados con la función
stepinfo de Matlab.

------------20200205_KPIResult_OrigModel-----------------------------------------

Contiene los valores de los KPIs calculados con la función perfomanceTemp() by my.
Esta funcion no se encuentra en esta carpeta, por tanto importante agragarla al path.
