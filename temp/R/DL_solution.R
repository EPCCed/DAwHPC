library(ggplot2)
setwd("/Users/msabate/MSc/2018-2019/DL_practical")
data = read.table("data.txt", sep=",", header = TRUE)

p = ggplot(data=data, aes(x1,x2, color=factor(y))) + geom_point() 
print(p)

model = glm(formula = y~x1+x2, data = data, family = "binomial")

grid = expand.grid(x1 = seq(min(data$x1), max(data$x1), 0.02),
                   x2 = seq(min(data$x2), max(data$x2), 0.02))

y_grid = predict(model, grid, type="response")
y_grid_binary = as.numeric(y_grid>0.5)

grid$y = y_grid_binary

p = ggplot(data=data, aes(x1,x2, color=factor(y))) + geom_point(size=1) 
p = p + geom_point(data=grid, aes(x1, x2, color=factor(y)), alpha=0.1)
print(p)



# activation function
sigmoid <- function(z){
  output = 1/(1+exp(-z))
  return(output)
}



# forward model
forward_model <- function(model, x){
  # model is a list with the following 
  # x is the input
  W1 = model[['W1']]
  b1 = model[['b1']]
  W2 = model[['W2']]
  b2 = model[['b2']]
  
  # forward pass
  # hidden layer
  z2 = W1 %*% t(x) + b1
  a2 = sigmoid(z2)
  
  # output layer
  z3 = W2 %*% a2 + b2
  a3 = sigmoid(z3)
  output = list(z2 = t(z2), a2=t(a2), z3=t(z2), a3=t(a3)) # we transpose so that every row is the output of the model applied to each observation
  
  return(output)
}


loss_fn <- function(model, x, y){
  layers_model = forward_model(model, x)
  y_pred = layers_model[['a3']]
  loss = y * log(y_pred) + (1-y) * log(1-y_pred)
  return(sum(-loss))
}


GD_step <- function(model, x, y, lr=0.001){
  W1 = model[['W1']]
  b1 = model[['b1']]
  W2 = model[['W2']]
  b2 = model[['b2']]
  
  pred_model = forward_model(model, x)
  z2 = pred_model[['z2']]
  a2 = pred_model[['a2']]
  z3 = pred_model[['z3']]
  a3 = pred_model[['a3']]
  
  delta3 = a3 - y
  dW2 = t(a2) %*% delta3
  db2 = apply(FUN=sum, X=delta3, MARGIN=2)
  
  delta2 = sigmoid(z2) * (1-sigmoid(z2)) * (delta3%*%W2)
  dW1 = t(x) %*% delta2
  db1 = apply(FUN=sum, X=delta2, MARGIN=2)
  
  W2 = W2 - lr * t(dW2)
  b2 = b2 - lr * db2
  W1 = W1 - lr * t(dW1)
  b1 = b1 - lr * db1
  
  model[['W1']] = W1
  model[['b1']] = b1
  model[['W2']] = W2
  model[['b2']] = b2
  
  return(model)
}


train <- function(model, n_epochs, x, y){
  for(epoch in 1:n_epochs){
    model = GD_step(model, x=x, y=y)
    loss = loss_fn(model, x=x, y=y)
    
    if(epoch %% 10 == 0){
      log = paste("Epoch: ", epoch, "/", n_epochs,", loss: ", loss, sep="")
      print(log)
    }
  }
  return(model)
}


# we initialise things
n_hidden = 30
matrix
W1 = matrix(data=rnorm(2*n_hidden), nrow=n_hidden, ncol=2)
b1 = rnorm(n_hidden)
W2 = matrix(data=rnorm(n_hidden), nrow=1, ncol=n_hidden)
b2 = rnorm(1)
model = list(W1 = W1, b1=b1, W2=W2, b2=b2)


model = train(model=model, n_epochs=5000, x=as.matrix(x=data[,c("x1", "x2")]), y=c(x=data$y))


grid = expand.grid(x1 = seq(min(data$x1), max(data$x1), 0.02),
                   x2 = seq(min(data$x2), max(data$x2), 0.02))
y_grid = forward_model(model, x=as.matrix(grid))[['a3']]
y_grid_binary = y_grid>0.5
grid$y = as.numeric(y_grid_binary)

p = ggplot(data=data, aes(x1,x2, color=factor(y))) + geom_point(size=1) 
p = p + geom_point(data=grid, aes(x1, x2, color=factor(y)), alpha=0.1)
print(p)




