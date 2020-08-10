function x0=Newton_Raphson(St0,Ht0,G,C,E,P,a)
    x0=0;
    x1=St0;
    while(abs(x0-x1)>0.001)
        x0=x1-profit_mineur2(x1,Ht0,G,C,E,P,a)/...
            derivee_profit_mineur(x1,Ht0,G,C,E,P,a);
        x0=x0+x1;
        x1=x0-x1;
        x0=x0-x1;
    end
end