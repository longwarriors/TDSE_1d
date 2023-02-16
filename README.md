# TDSE_1d
###### 一维含时薛定谔方程(time depedent Schrödinger equation, TDSE)的Crank-Nelson格式数值解  
含时演化需要保证波函数的归一性不变，因此离散格式不能是向前欧拉(explicit)或向后欧拉(implicit)，而采用Crank-Nelson方法，保证波函数演化步骤不发散，维持概率守恒：
$$
|\psi(t+\Delta t)|^2=|\psi(t)|^2
$$
***高斯波包势垒穿透***
***谐振子势***