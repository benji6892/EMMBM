function f=estimation_parametres_objectif_hf(param,R,Q,d,f,h,alpha,sigma2,r,precision)
    a=param(1);
    I=param(2);
    Q_sim=simulation_Q_hf(R,Q(d-1),d,f,h,a,r,I,alpha,sigma2,precision);
    vrai_Q=Q(d:f);
    f=norm((Q_sim-vrai_Q)./vrai_Q);
end