% Simulate investment barrier with finite horizon of 2 years

%% SECTION 1: Environment / Initialization / Parameters

clearvars;
close all;

%----% Flags %------------------------------------------------------------%
%

version         = 0;
revision        = 0;
date            = 'July, 2019';

kpic            = 1;
flag_pic        = 1;                                                        % 1 = debug mode 
flag_approx     = 1;                                                        % 1 = polynomial approximation of barrier (needs curve fitting toolbox)
flag_check      = 0;                                                        % 1 = check that the barrier is accurate 

% Script header
disp(' ');
disp('Bitcoin Barrier finite horizon');
disp(' ');
tag          = sprintf('Date...................: %s', date); disp(tag);
tag          = sprintf('Version................: %2.1f.%1.0f', version, revision); disp(tag);
disp(' ');

%-----% Main parameters %-------------------------------------------------%



r               = 0.24/4;                                                     % Annual time discounting


% Parameters of Brownian

% Daily estimates
est_daily_alpha  = 0.001419;
est_daily_a      = 0.0021;
est_daily_sigma2 = 0.001433;

%Quarterly estimates
alpha           = est_daily_alpha*365/4;                                                       % Trend brownian
a               = est_daily_a*365/4;                                                         % Rate technological progress
mu              = alpha+a;
sigma           = sqrt(est_daily_sigma2*365/4);



%Evaluate the caracteristic equation of the Cauchy-Euler equation

coef            = [sigma^2/2 (mu-sigma^2/2) -r-a];
beta            = roots(coef);
beta1           = max(beta);                                               % Positive root
beta2           = min(beta);                                               % Negative root (unused)

% Investment Costs
I               = 1;
I_T             = 1;
eta             = 30;
%----------------------% Grid parameters%-----------------------------%

% Time horizon
horizon         = 5;                                                       % Time horizon (4 years=16 quarters)        

% Discretization of time 
tmin                        = 0;
tmax                        = horizon;
number_observation_quarter  = 100;
N                           = tmax*number_observation_quarter;                 % size of the grid (time)
deltat                      = (tmax-tmin)/N;                              % step (time)
Tmesh_n                     = tmax:-deltat:tmin;                            % Descending order (CAUTION!)

% Generate cost vector

I_vec           = ones(length(Tmesh_n));

%-----% Create a structure for the parameters %---------------------------%

par.r           = r;
par.I           = I;
par.mu          = mu;
par.sigma       = sigma;


%% SECTION 2: Build Time Dependent Barrier 

disp(' ')
        
%---------%Store variables%----------------------------------------------%
 
Barrier_buffer       = zeros(N+1,1);
Barrier_norm_buffer  = zeros(N+1,1);
if flag_approx==1
Barrier_apx_buffer   = zeros(N+1,1);
end

% Generate cost vector
I_mesh  = I_vec*I_T;

% The model is solved backward. 

% Step 1: Evaluate R (reservation productivity at the final date t=T in the last iteration period)

P_bar             = (beta1/(beta1-1))*I_T*(r-alpha);

V_fun           = @(P) P./(r-alpha)-(I_T/(beta1-1))*((P)/((beta1/(beta1-1))*I_T*(r-alpha)))^beta1;


Sol_fun         = @(P) (P<P_bar)*(V_fun (P))+...  % Merge 2 solutions
                        (P>=P_bar)*I_T;

% Generate grids

% Discretization of productivity (log) (index i)
Pmin            = 0;
% Productivity grid including PstarT
Pmax                        = P_bar*5;
deltaP                      = (Pmax-Pmin)/200;
Pmesh                       = Pmin:deltaP:Pmax;
M                           = length(Pmesh)-1; 

Solution_mesh_buffer    = zeros(N+1,M+1);    
Investment_mesh_buffer  = zeros(N+1,M+1);  

% Time vector
Tmesh                       = tmax:-deltat:tmin;                            % Descending order (CAUTION!)

% Step 2: Evaluate R(t) (Time moving Barrier)
%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Set: Buffer for time and productivity %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Set: buffers for V(i,j), productivity, time
Solution_mesh               = Solution_mesh_buffer;
Investment_mesh             = Investment_mesh_buffer;  
Solution_mesh(:)            = NaN;                                          % for test purpose only! 

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Set: Terminal and boundary conditions %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Terminal condition at t=T
Solution_mesh(1,:) = Pmesh/r;
for i = 1:length(Pmesh)
    
        P                       = Pmesh(i); 
        SolT                    = Sol_fun(P);   
        Solution_mesh(1,i)      = SolT;
    
end

% Boundary conditions at P=Pmin and P=Pmax (loop over t (time))
for j = 1:length(Tmesh)
    Solution_mesh(j,1)      = 0;          % BC at P = Pmin ---> S(Pmin) = 0
end

Solution_mesh(1:2,M+1)    = Sol_fun(Pmax);          % BC at P = Pmax and T=Tmax = 0 
    

%omega                       = 1.2;                                         % Relaxation parameter (1 = Gauss-Seidel)
tolerance                   = 1e-3;

% loop over time (except for the terminal date that is already known). Last
% iteration will fill the last row of the matrix.

max_iter                    = 200;
check_iter                  = zeros(N,1);

for j = 1:N
j

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Build: Generating functions and tridiagonal matrix %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% generating function for the linear system (in state space )
% fun_a               = @(i) 0.5*deltat*((alpha+a+Investment_mesh(i))*i-sigma^2*i^2);                   % coef
% fun_b               = @(i) 1+Investment_mesh(i)*deltat+(sigma^2*i^2+(r+a))*deltat;                % coef
% fun_c               = @(i) -0.5*(sigma^2*i^2+(alpha+a+Investment_mesh(i))*i)*deltat;                  % coef
% fun_d               = @(i) (i*deltaP+eta*Investment_mesh(i)^(1+eta))*deltat;                       

% generating function for the linear system (in state space )
% Do not correct for approximation of investment policy!
fun_a               = @(i) 0.5*((alpha+a-(i>0)*Investment_mesh(j,max(1,i)))*i-sigma^2*i^2)*deltat;                   % coef
fun_b               = @(i) 1+(sigma^2*i^2+(r+a))*deltat;                % coef
fun_c               = @(i) -0.5*(sigma^2*i^2+(alpha+a-(i>0)*Investment_mesh(j,max(1,i)))*i)*deltat;                  % coef
fun_d               = @(i) (i*deltaP+(i>0)*eta*Investment_mesh(j,max(1,i))^(1+eta))*deltat;                       

% fun_a               = @(i) 0.5*deltat*((alpha+a)*i-sigma^2*i^2);                   % coef
% fun_b               = @(i) 1+(sigma^2*i^2+(r+a))*deltat;                % coef
% fun_c               = @(i) -0.5*(sigma^2*i^2+(alpha+a)*i)*deltat;                  % coef
% fun_d               = @(i) (i*deltaP)*deltat;                          % constant (CAUTION! fun_d is time dependent if flag_epl == 1)

% Tridiagonal matrix
Acoeffs             = zeros(M+1,1);
Bcoeffs             = zeros(M+1,1);
Ccoeffs             = zeros(M+1,1);
Dconsts             = zeros(M+1,1);

for i = 1:M+1
   Acoeffs(i)           = fun_a(i-1);
   Bcoeffs(i)           = fun_b(i-1);
   Ccoeffs(i)           = fun_c(i-1);
   Dconsts(i)           = fun_d(i-1);
end

% Tri is (M-1)*(M-1) matrix
L                   = diag(Acoeffs(3:M),-1);                                % Lower part of the Tridiagonal matrix
D                   = diag(Bcoeffs(2:M));                                   % Diagonal part
U                   = diag(Ccoeffs(2:M-1),+1);                              % Upper part

Tri                 = L+D+U;
TT                  = D\(L+U);                                              % D^-1*(L+U)

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Gauss-Seidel/Successive Over Relaxation (SOR) method %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Calculate: optimal relaxation parameter
% use theorem 7.26 in Burden and Faires (2011)
spectral_norm               = max(sqrt(eig(TT'*TT)));
t1                          = 2;
t2                          = 1+sqrt(1-spectral_norm^2);
omega                       = t1/t2;


    % Set RHS (incl. constants terms)
    vec_consts              = zeros(M-1,1);
    vec_consts(1,1)         = fun_a(0)*Solution_mesh(j+1,1)-Dconsts(2);
%    vec_consts(1,1)         = fun_a(0)*Solution_mesh(j+1,1);
    vec_consts(M-1,1)       = fun_c(M)*Solution_mesh(j+1,M+1)-Dconsts(M);
%    vec_consts(M-1,1)       = fun_c(M)*Solution_mesh(j+1,M+1);
   vec_consts(2:M-2,1)     = -Dconsts(3:M-1);
   
    RHS                     = Solution_mesh(j,2:M)'-vec_consts;
    
    % Solving Ax=b iteratively using SOR method
    A                       = Tri;
    b                       = RHS;
   
    x                       = Solution_mesh(j,2:M)';
    %x0                      = zeros(size(x));
    x0                      = x;
    n_iter                  = 0;                                            % Reset n_iter
    error                   = 1;
    
    n                       = length(b);
    while (error > tolerance)&&(n_iter < max_iter)
       n_iter                   = n_iter+1; 
       
       for i = 1:n
          x(i)      = b(i)-A(i,1:i-1)*x(1:i-1)-A(i,i+1:n)*x0(i+1:n);
          x(i)      = x(i)/A(i,i);
          x(i)      = omega*x(i)+(1-omega)*x0(i);         % Check for Barrier
%          x(i)      = min(omega*x(i)+(1-omega)*x0(i),I_T);
 
       end
       error    = norm(x-x0);
       x0       = x;
       
    end
    check_iter(j)                   = n_iter; 
    Solution_mesh(j+1,(2:end-1))  = x;
    
    Solution_mesh(j+1, end)       = interp1(Pmesh(1:end-1),Solution_mesh(j+1,1:end-1),Pmesh(end),'linear','extrap');
    if j<N
    Solution_mesh(j+2, end)       = interp1(Pmesh(1:end-1),Solution_mesh(j+1,1:end-1),Pmesh(end),'linear','extrap');
    end
    Investment_mesh(j+1, :)       = (max(0,Solution_mesh(j+1,:)-1)/(1+eta)).^(1/eta);
    
end


figure
plot(Pmesh,Solution_mesh(end,:),'Linewidth',2)
hold on
plot(Pmesh,Solution_mesh(1,:),'Linewidth',2)
xlim([0 P_bar+.1])

figure
plot(Pmesh,Investment_mesh(end,:),'Linewidth',2)
hold on
plot(Pmesh,Investment_mesh(1,:),'Linewidth',2)

figure
plot(Pmesh,Solution_mesh(end, :),'Linewidth',2)
hold on
plot(Pmesh,Solution_mesh(end-10, :),'Linewidth',2)
plot(Pmesh,Solution_mesh(end-20, :),'Linewidth',2)

return

if flag_check == 1
tag          = sprintf('   SOR: maximum number of iterations %2.0f', max(check_iter)); disp(tag);
end

% Check for barrier (loop over t)
Barrier      = zeros(N+1,1);
for i = 1:N+1
    index         = find(Solution_mesh(i,:)>=I_mesh(end+1-i),1,'first');
    Barrier(i)    = Pmesh(index);
end

% Polynomial approx.
Y_p_org           = Barrier;

% Set vectors in ascending order!
Time              = flipud(Tmesh');
Barrier_org       = flipud(Y_p_org);                                        % Barrier (original form)

% Approximation of Barrier
if flag_approx==1
% Double exponential approx. (Use Curfitting Toolbox)
% h(t)   = a*exp(b*t)+c*exp(d*t)
% h'(t)  = a*b*exp(b*t)+c*d*exp(d*t)

x               = flipud(Tmesh');
y               = flipud(Barrier);
h               = fit(x,y,'exp2');
coefh           = coeffvalues(h);

a_apx               = coefh(1);
b_apx               = coefh(2);
c_apx               = coefh(3);
d_apx               = coefh(4);
Y_apx               = a_apx*exp(b_apx*Tmesh)+c_apx*exp(d_apx*Tmesh);

Barrier_apx         = flipud(Y_apx');                                           % Barrier (approximation)
end

% Detrended Barriers
Barrier_detrended       = Barrier_org'.*exp(-a.*Tmesh_n-a.*horizon*(N_T-t));
Barrier_apx_detrended   = Barrier_apx'.*exp(-a.*Tmesh_n-a.*horizon*(N_T-t));

% Store Solutions
Solution_mesh_buffer{t} = Solution_mesh;    
Barrier_buffer{t}       = Barrier_org;
Barrier_norm_buffer{t}  = Barrier_org/(1+(t>1)*(-1));
if flag_approx==1
Barrier_apx_buffer{t}   = Barrier_apx;
end
Barrier_det_buffer{t}   = Barrier_detrended;
Barrier_apx_det_buffer{t}= Barrier_apx_detrended;



%% SECTION 3: Merge barriers and draw figures

% Barrier for all the periods
Barrier_merged      = reshape(cell2mat( Barrier_buffer),1,(N+1)*N_T);
Barrier_apx_merged  = reshape(cell2mat( Barrier_buffer),1,(N+1)*N_T);

Barrier_det_merged     = reshape(cell2mat( Barrier_det_buffer),1,(N+1)*N_T);
Barrier_apx_det_merged = reshape(cell2mat( Barrier_apx_det_buffer),1,(N+1)*N_T);

% Barrier for all the periods with renormalization
Barrier_merged_norm = reshape(cell2mat( Barrier_norm_buffer),1,(N+1)*N_T);

% Time vector for all periods
Time_merged   = deltat:deltat:deltat*length(Barrier_merged);
Time_merged   = Time_merged-deltat;



if flag_pic == 1
figure(kpic)
kpic = kpic+1;
plot(Time_merged ,Barrier_merged  ,'LineWidth',3,'Color',[1 0.388235 0.278431])
hold on
plot(Time_merged ,Barrier_apx_merged ,'LineWidth',3,'Color',[1 0.388235 0.278431])
xlabel('Quarters')
ylabel('R(t)')
title('barrier ')
axis tight
grid on
print -depsc fig_Barrier.eps
print -dpdf fig_Barrier.pdf
end

if flag_pic == 1
figure(kpic)
kpic = kpic+1;
plot(Time_merged ,Barrier_det_merged ,'LineWidth',3,'Color',[1 0.388235 0.278431])
hold on
plot(Time_merged ,Barrier_apx_det_merged,'LineWidth',3,'Color',[1 0.388235 0.278431])
xlabel('Quarters')
ylabel('R(t)')
title('barrier ')
axis tight
grid on
print -depsc fig_Barrier_det.eps
print -dpdf fig_Barrier_det.pdf
end


if flag_pic == 1
figure(kpic)
kpic = kpic+1;
plot(Time_merged ,Barrier_merged_norm  ,'LineWidth',3,'Color',[1 0.388235 0.278431])
xlabel('Quarters')
ylabel('R(t)')
title('Normalized barrier')
axis tight
grid on
print -depsc fig_Barrier_det.eps
print -dpdf fig_Barrier_det.pdf
end

return

if flag_pic == 1
figure(kpic)
kpic = kpic+1;
plot(fliplr(Tmesh),Barrier_org_detrended,'LineWidth',3,'Color',[1 0.388235 0.278431])
hold on
plot(fliplr(Tmesh),Barrier_apx_detrended,'LineWidth',3,'Color',[1 0.388235 0.278431])
xlabel('Quarters')
ylabel('R(t)')
title('barrier detrended')
axis tight
grid on
print -depsc fig_Barrier_nonnorm.eps
print -dpdf fig_Barrier_nonnorm.pdf
end


if flag_pic == 1
figure(kpic)
kpic = kpic+1;
plot(Time_merged,Barrier_merged,'LineWidth',3,'Color',[1 0.388235 0.278431])
xlabel('Quarters')
ylabel('R(t)')
title('barrier without renormalization')
axis tight
grid on
print -depsc fig_Barrier_nonnorm.eps
print -dpdf fig_Barrier_nonnorm.pdf
end

if flag_pic == 1
figure(kpic)
kpic = kpic+1;
plot(Time_merged,Barrier_merged_norm,'LineWidth',3,'Color',[1 0.388235 0.278431])
xlabel('Quarters')
ylabel('R(t)')
title('barrier with renormalization')
axis tight
grid on
print -depsc fig_Barrier_norm.eps
print -dpdf fig_Barrier_norm.pdf
end

%% Section 4: Check barrier using closed-form solution for density

if flag_check ==1

 % Select timing of barrier to evaluta
 % Default choice is initial barrier, i.e. t=1
   
time_check  = 1;

    for  i=1:length(Tmesh)-1

        Barrier_check(i) = Barrier_buffer{time_check }(end-i);
        Exp_ret_fun      = @(t) exp(-r.*t).*esp_pt(t,Barrier_buffer{time_check }(end-i),mu,sigma^2,0);
        Exp_ret(i)       = integral(Exp_ret_fun ,0,deltat ,'ArrayValued',true);
        Cont_V_fun       = @(x) interp1(Pmesh,Solution_mesh_buffer{time_check}(i,:),x); % Note index for solution_mesh is backward in time
        Exp_cont_fun     = @(x) exp(-r.*deltat).*Cont_V_fun(x).*densite_Pt(x,deltat,Barrier_buffer{time_check}(end+1-i),mu,sigma^2,0);

        Exp_cont_val(i)  = integral(Exp_cont_fun,0,Barrier_buffer{time_check}(end+1-i)); % Note integrate w.r.t. barrier next period

        Exp_payoffs(i)   = Exp_ret(i)+Exp_cont_val(i)

    end

% Approximation errors

Approx_error        = Exp_payoffs-I;

end

