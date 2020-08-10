a=0.00207;
sigma2=0.0012915;

r=0.1/365;
I=1825;
mu=0.000615;
alpha=mu+0.5*sigma2;
horizon=647;
precision=10;

[Bt,P_star_T]=simu_horizon_fini(a,r,I,alpha,sigma2,horizon,precision);

plot(Bt);


