function f=estimation_parametres_objectif_constrained_v2(param,eta,R,Q,d,f,alpha,sigma2,r)
    
    
    length_time          = param(1);
    a                    = param(2);
    scale                = param(3);
    
    param_init =[param, eta, scale];
    
    [Pmesh, policy, cutoff]=Simu_policy_constrained_v1(param_init,alpha,sigma2,r);
    
    barrier_guess   = 4.1344525933912921;
    Cost_guess      = barrier_guess/cutoff;
    
    options=optimset('tolX',1.0e-5,'tolFun',1.0e-3,'MaxIter',200);
    distance_fun = @(Cost)distance_constrained(Pmesh, policy, cutoff, Cost, length_time, a, Q, R, d, f);
    [cost, fval] = fminsearch(distance_fun,Cost_guess,options);

     f = fval;
end