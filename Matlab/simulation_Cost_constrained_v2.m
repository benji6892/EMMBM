function Cost_sim=simulation_Cost_constrained_v2(Pmesh, policy, cutoff, cost, scale, a, Q0, R, d, f,eta)
    
    % d: debut de la periode
    % f: fin de la periode
    % h: date du halving. (1420 et 2739)
    Rp=144*R(d:f); 
    
    Q_sim    = NaN(1,length(Rp));
    Cost_sim = NaN(1,length(Rp));
    
    Q_sim(1)=Q0;
    
    
    t_vec    = 1:length(Rp);
    
    cost_t = cost*exp(-a*t_vec/365);
    daily_cost = cost*365;
    Cost_sim(1) = daily_cost;
    
    for t=2:length(Rp)
        if Rp(t)/(Q_sim(t-1)*cost_t(t))<cutoff
            Q_sim(t) = Q_sim(t-1);
            Cost_sim(t) = daily_cost;
        else
            Q_sim(t)=min(Rp(t)/(cutoff*cost_t(t)),Q_sim(t-1)*(1+interp1(Pmesh,policy,Rp(t)/(Q_sim(t-1)*cost_t(t)))/365));
            Cost_sim(t) = daily_cost*(1+(1+eta)*((Q_sim(t)-Q_sim(t-1))/(scale^(-1/eta)*Q_sim(t)/365))^eta);
        end
    end
    
end