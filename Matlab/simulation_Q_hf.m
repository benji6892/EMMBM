function Q_sim=simulation_Q_hf(R,Q0,d,f,h,a,r,I,alpha,sigma2,precision)
    
    % d: debut de la periode
    % f: fin de la periode
    % h: date du halving. (1420 et 2739)
    Rp=144*R(d:f); 
    
    [Bt,P_star_T]=simu_horizon_fini(a,r,I,alpha,sigma2,h-d,precision);
    Bt=[Bt;P_star_T*R(h)/R(h-1)]; % on ajoute le jour du halving
    
    suite=P_star_T*exp(-a*(2:1:f-h)')/2;
    Bt=[Bt;suite];
    
    T=f-d+1;
    Q_sim=zeros(T+1,1);
    Q_sim(1)=Q0;
    for t=1:T
        Q_sim(t+1)=max(Q_sim(t),Rp(t)/Bt(t));
    end
    Q_sim=Q_sim(2:(T+1));    
end