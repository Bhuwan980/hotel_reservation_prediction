import lightgbm as lgb
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import uniform, randint

def get_lightgbm_model():
    """
    Returns a LightGBM model with default parameters.
    """
    model = lgb.LGBMClassifier(random_state=45)
    return model

def get_random_search_params():
    """
    Returns the parameters for RandomizedSearchCV to tune the LightGBM model.
    """
    param_dist = {
        'num_leaves': randint(20, 150),
        'max_depth': randint(3, 15),
        'learning_rate': uniform(0.01, 0.2),
        'n_estimators': randint(50, 500),
        'subsample': uniform(0.5, 1),
        'colsample_bytree': uniform(0.5, 1),
    }
    return param_dist

def get_random_search(model, param_dist, X_train, y_train, n_iter=10, cv=3, n_jobs=-1, random_state=45):
    """
    Returns the RandomizedSearchCV object after fitting.
    """
    random_search = RandomizedSearchCV(
        model, 
        param_distributions=param_dist, 
        n_iter=n_iter, 
        cv=cv, 
        verbose=2, 
        n_jobs=n_jobs, 
        random_state=random_state
    )
    random_search.fit(X_train, y_train)
    return random_search