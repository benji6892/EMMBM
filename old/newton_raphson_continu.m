function xs=newton_raphson_continu(C0,P0,a,R)
    xi=0.0001;
    xs=10000;
    while (profit_continu(xi,C0,P0,a,R)<0)
        xi=xi/2;
    end
    while (profit_continu(xs,C0,P0,a,R)>0)
        xs=2*xs;
    end
    while (xs-xi>0.0001)
        x=0.5*(xs+xi);
        profit=profit_continu(x,C0,P0,a,R);
        if (profit>0)
            xi=x;
        else
            xs=x;
        end
    end   
end


%  x0=0;
%     x1=0.001;
%     while(abs(x0-x1)>0.0001)
%         x0=x1-x1*(R/x1-(C0/a)*log(1+a*R/(C0*x1))-P0)/...
%             ((R/x1-(C0/a)*log(1+a*R/(C0*x1))-P0)+x1*(C0*R/(C0*x1^2+a*R)-R/(x1^2)));
%         x0=x0+x1;
%         x1=x0-x1;
%         x0=x0-x1;
%     end   