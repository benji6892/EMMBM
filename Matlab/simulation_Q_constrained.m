function Q_sim=simulation_Q_constrained(Pmesh, policy, cutoff, cost, length_time, a, Q0, R, d, f)
    
    % d: debut de la periode
    % f: fin de la periode
    % h: date du halving. (1420 et 2739)
    Rp=144*R(d:f); 
    
    Q_sim = NaN(1,length(Rp));
    
    Q_sim(1)=Q0;
    
    t_vec    = 1:length(Rp);
    
    cost_t = cost*exp(-a*t_vec/365);
        
    for t=2:length(Rp)
        if Rp(t)/(Q_sim(t-1)*cost_t(t))<cutoff
            Q_sim(t) = Q_sim(t-1);
        else
            Q_sim(t)=min(Rp(t)/(cutoff*cost_t(t)),Q_sim(t-1)*(1+interp1(Pmesh,policy,Rp(t)/(Q_sim(t-1)*cost_t(t)))/(365*length_time)));
        end
    end
    
end