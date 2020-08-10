function arg=estimation_parametres_hf(param_init,R,Q,d,f,h,alpha,sigma2,r,precision)

    options=optimset('display','iter-detailed','tolX',1.0e-5,'tolFun',1.0e-3,'MaxIter',200);
    objectif=@(param)estimation_parametres_objectif_hf(param,R,Q,d,f,h,alpha,sigma2,r,precision);
    arg=fminsearch(objectif,param_init,options);
end

