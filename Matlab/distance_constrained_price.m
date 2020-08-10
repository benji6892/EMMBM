function distance=distance_constrained_price(Pmesh, policy, cutoff, cost, length_time, eta, a, Q, R, d, f,...
                                             Dates_ASICS, Price_ASICS)
    
                                         
    % d: debut de la periode
    % f: fin de la periode
    % h: date du halving. (1420 et 2739)
    Rp=144*R(d:f); 
    
    Q_sim = NaN(1,length(Rp));
    
    Q0=Q(d-1);
    Q_sim(1)=Q0;
    
    t_vec    = 1:length(Rp);
    
    cost_t = cost*exp(-a*t_vec/365);
    daily_cost = cost*365*length_time;
    Cost_sim(1) = daily_cost;
    
    I_d  = Price_ASICS(1)*exp(a*(Dates_ASICS(1)-d));
    Cr_d = daily_cost-I_d;
    Det_Price_ASICS = Price_ASICS.*exp(a*(Dates_ASICS-Dates_ASICS(1))/365);
    
    for t=2:length(Rp)
        if Rp(t)/(Q_sim(t-1)*cost_t(t))<cutoff
            Q_sim(t) = Q_sim(t-1);
            Cost_sim(t) = daily_cost;
        else
            Q_sim(t)=min(Rp(t)/(cutoff*cost_t(t)),Q_sim(t-1)*(1+interp1(Pmesh,policy,Rp(t)/(Q_sim(t-1)*cost_t(t)))/(365*length_time)));
            Cost_sim(t) = daily_cost*(1+(1+eta)*((Q_sim(t)-Q_sim(t-1))/(Q_sim(t)/(365*length_time)))^eta);
        end
    end
    
    I_t = Cost_sim - Cr_d;
    
    for i = 1 : length(Dates_ASICS)
        
        if Dates_ASICS(i)-15<d
            I_mean_ASICS_t(i) = I_t(Dates_ASICS(i)-d+1);
        elseif Dates_ASICS(i)+15>f
            I_mean_ASICS_t(i) = mean(I_t(Dates_ASICS(i)-d+1-15:Dates_ASICS(i)-d+1));
        else
            I_mean_ASICS_t(i) = mean(I_t(Dates_ASICS(i)-d+1-15 : Dates_ASICS(i)-d+1+15));
        end

    end
    
    distance_Q = norm((Q_sim'-Q(d:f))./Q(d:f));
    distance_P = norm((I_mean_ASICS_t-Det_Price_ASICS)./Det_Price_ASICS);
    distance   = distance_Q/length(Dates_ASICS)+distance_P;

end