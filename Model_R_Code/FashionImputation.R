library("softImpute")
library("reshape2")
library("Metrics")

setwd("/Users/BlackHawk/Desktop/Fashion BigDatathon/data/") # Change this to the directory where your data is
ratings = read.csv("star1 (1).csv")
ratings = as.matrix(ratings[,-1]) #take out the column with 

product_x_twitterbio = read.csv("twitterproduct_x_bio_matrix.txt")



twittersentiment = read.csv("tweetssentiment.txt", header = FALSE) #raw data, list of sentiments
colnames(twittersentiment) <- c("userid", "productid_hash", "tweet", 
                                "sentiment_score", "value type")
tw_rating = twittersentiment[,c("userid", "productid_hash", "sentiment_score")]

ratings = tw_rating #rating is the common variable used in script
# rating_training[,1] = as.character(rating_training[,1])
# rating_training[,2] = as.character(rating_training[,2])

drop_rate = 0.01
drop_rows = sample(1:nrow(twittersentiment),floor(nrow(twittersentiment)*drop_rate))
rating_test = twittersentiment[drop_rows,c("userid", "productid_hash", "sentiment_score")] #create our testing data
user_ids_test = as.character(rating_test[,1]) #We want to later get the columns by the same name
productids_test = as.character(rating_test[,2])

rating_training = as.matrix(ratings) #Needed to insert NAs
R_is_a_shitty_programming_language = as.numeric(rating_training[,3])
rating_training[drop_rows,3] <- NA #We will use these rows for testing, so need to impute

user_ids_train <- unique(rating_training[,1]) #store userids, will input them later
# Need to use transform to give users and products unique numeric ids, otherwise dcast (below) won't work
rating_training = transform(rating_training,userid=as.numeric(factor(rating_training[,1])))
# transform will automatically coerce to dataframe

product_ids_train <- unique(rating_training[,2]) #store productids, will input them later
rating_training = transform(rating_training,productid_hash=as.numeric(factor(rating_training[,2]))) 

rating_training[,3] = R_is_a_shitty_programming_language

rating_mat = dcast(as.data.frame(apply(as.matrix(rating_training),2,as.numeric)), userid ~ productid_hash, value.var = "sentiment_score", na.rm = FALSE, fun.aggregate = mean)  #cast to dataframe to use in reshape
rating_mat = rating_mat[,-1] #can drop the userid column, the names of rows are now useids
rownames(rating_mat) <- user_ids_train
colnames(rating_mat) <- product_ids_train

test_coordinates = cbind(user_ids_test, productids_test)

#---------- A function for getting the ratings given lists of user and movie ids --------#
get_coordinates <- function(x, i, j) {  
    v = {}
    for(m in 1:length(i)) {
        v = cbind(v, x[i[m],j[m]])
    }
    return(as.vector(v))
}
#-----------------------------------------------------------------------------------------#

max_lambda = lambda0(rating_mat) #This is the lambda that will return a 0 matrix, our lambda must be smaller
matrix_rank = floor(min(dim(rating_mat))/2)
#result_parts = 0

#-------- Calculate vectors of actual (testing) data and predicted (training) data ------#
# lam = lambda; method = "svd" or "als"
get_actual_and_predicted <- function(lam, method, training, rn, cn, testing, mr) {
    
    result_parts <<- softImpute(as.matrix(training), rank.max = mr, lambda = lam, type = method) #returns UDV
    imputed <<- as.matrix(result_parts$u) %*% diag(result_parts$d) %*% t(as.matrix(result_parts$v))
    # <<- in R means write as global variable (can be accessed outside function)
    # even though the last value in result_parts$d is always a 0, it's better to keep it than remove it
    
    rownames(imputed) <<- rn
    colnames(imputed) <<- cn
    
    actual = testing[,3]  # Taken from our testing data
    predicted = get_coordinates(imputed, user_ids_test, productids_test) # Get the values we predicted with our imputation
    
    return(cbind(actual, predicted))
}
#-----------------------------------------------------------------------------------------#

#---------- We will use the below function for testing different values of lambda -------#
testing_lambda = function(max_lam, training, rn, cn, testing, mr, type) {
    # ------ Tunning Parameters --------#
    max_lam = max_lam / 50
    step = 2  #this is the amount we will increase lambda with each iteration - large means faster convergence
    iterations = 30 #number of for loop iterations
    #-----------------------------------#
    #------------- set up --------------#
    lambda = {}
    soft_result = {}
    type.method = "svd" # our default method
    type.lambda = 0  # our default lambda
    #-----------------------------------#
    
    for(i in 1:iterations) {
        switch(type,  # This switch statement will make the function slower, but the code simpler
               soft = {
                   type.lambda = max_lam*i*step
               },
               hard = 1,
               als = {
                   type.lambda = max_lam*i*step
                   type.method = "als"
               })
        
        ap = get_actual_and_predicted(type.lambda, type.method, training, rn, cn, testing, mr)
        RMSE = rmse(ap[,1], ap[,2])  #Calculate the difference (error) btwn the values we predicted and actual values
        
        print(c("Soft RMSE for lambda = ", type.lambda, " is : ", RMSE, " i is: ", i))
        
        lambda[i] = type.lambda
        soft_result[i] = RMSE
    }
    return(cbind(lambda, soft_result))  #return the lambdas and their corresponding error rates that were tested
}
#----------------------------------------------------------------------------------#

get_best_lambda <- function(data) {
    min_error_index = which.min(data[,2])
    best_lambda = data[min_error_index, 1]
    return(c(best_lambda, data[min_error_index, 2]))
}


#--------------------------- Soft SVD -----------------------------#
lambdas_and_errors = testing_lambda(1, rating_mat, user_ids_train, 
                                    product_ids_train, rating_test, matrix_rank, type = "soft")
#get_actual_and_predicted: (lam, method, training, rn, cn, testing, mr)
soft_lambda = get_best_lambda(lambdas_and_errors)[1]
ap = get_actual_and_predicted(1, method = "svd", rating_mat, user_ids_train, 
                              product_ids_train, rating_test, matrix_rank)
soft_RMSE = rmse(ap[,1], ap[,2])  #Calculate the difference (error) btwn the values we predicted and actual values

Final_ranking_list = as.matrix(colSums(imputed)[1:50])

setwd("/Users/BlackHawk/Desktop/") # Change this to the directory where your data is
write.csv(Final_ranking_list, "Final_fashion_rankings.csv")
    
    
    
