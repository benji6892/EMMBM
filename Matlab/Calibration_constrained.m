% Main code for problem with onvex constraint
clear all 
close all


%% Load DATA
donnees=xlsread('database');
R=donnees(:,1);
Q=donnees(:,3);



%% Guessed parameters; Annual values

% TP
a           =0.69594537446421012; %0.0032334 

% Adjt Costs
eta         = 30;
scale       = 1;

% Brownian Parameters; Annual Values
alpha       =0.91582303693997913; %0.0065322 
sigma2      =0.696228159836; %0.0053494 

mu          = alpha+a;

% Discount Rate
r           =0.1;

% Starting and final dates
d=2091; %812 
f=3750; %1483 


%% Estimation

% grid search

length_vec = 1/8:1/8:3/4;
a_vec      = a-.1:.05:a+.1;
eta_vec    = 6:4:20;

Distance_mat = NaN(length(length_vec),length(a_vec),length(eta_vec));

for i=1:length(length_vec)
    for j=1:length(a_vec)
        parfor k =1:length(eta_vec)
        step=[i,j,k],
        disp(step)
        param_init =[length_vec(i),a_vec(j),eta_vec(k)]
        Distance_mat(i,j,k)=estimation_parametres_objectif_constrained(param_init,scale,R,Q,d,f,alpha,sigma2,r);
        end
    end
end

[min_val,idx]       = min(Distance_mat(:));
[row,col,tri]       = ind2sub(size(Distance_mat),idx);

length_vec_guess    = length_vec(row);
a_guess             = a_vec(col);
eta_guess           = eta_vec(tri);

% Minimization
options                 = optimset('display','iter-detailed','tolX',1.0e-5,'tolFun',1.0e-3,'MaxIter',200);
objectif                = @(param)estimation_parametres_objectif_constrained(param,scale,R,Q,d,f,alpha,sigma2,r);

param_init              = [length_vec_guess,a_guess,eta_guess]
[param_opt, obj_val]    = fminsearch(objectif,param_init,options);


% Illustration

parameters_optimal      = [param_opt,scale];

[Pmesh, policy, cutoff] = Simu_policy_constrained_v1(parameters_optimal,alpha,sigma2,r);

figure
plot(Pmesh,policy,'Linewidth',2)
xlabel('P')
ylabel('Policy')
axis tight

barrier_guess   = 4.1344525933912921;
Cost_guess      = barrier_guess/cutoff;
    
options         =optimset('tolX',1.0e-5,'tolFun',1.0e-3,'MaxIter',200);
distance_fun    = @(Cost)distance_constrained(Pmesh, policy, cutoff, Cost, param_opt(1), param_opt(2), Q, R, d, f);
[cost_opt, fval]= fminsearch(distance_fun,Cost_guess,options);

Q0=Q(d-1);

Q_sim = simulation_Q_constrained(Pmesh, policy, cutoff, cost_opt, length_time, a, Q0, R, d, f);

figure
plot(d:f,log(Q_sim),'Linewidth',2)
hold on
plot(d:f,log(Q(d:f)),'Linewidth',2)
xlabel('Time')
ylabel('Q_t')
legend('Simulation','Data')

% Back-out values

b               = 1/param_opt(1);

a               = param_opt(2);

K_0             = cost_opt*365*param_opt(1);

return