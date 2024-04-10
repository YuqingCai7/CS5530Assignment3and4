library(tidyverse)

raw_data <- read.csv("C:/Users/yuqin/Desktop/CS5530/CS5530Assignment3and4/Cai - DiabetesProject/data_raw/diabetes.csv")
glimpse(raw_data)

set.seed(123)

sample_data <- raw_data %>% 
  sample_n(25)

sample_mean <- mean(sample_data$Glucose)
sample_max <- max(sample_data$Glucose)

population_mean <- mean(raw_data$Glucose)
population_max <- max(raw_data$Glucose)

glucose_comparison <- data.frame (
  Statistic = c("mean Glucose", "highest Glucose"),
  Sample = c(sample_mean, sample_max),
  Population = c(population_mean, population_max)
)

long_data <- glucose_comparison %>% 
  pivot_longer(-Statistic, names_to = "Group", values_to = "Value")

ggplot(long_data, aes(x = Statistic, y = Value, fill = Group)) + 
  geom_bar(stat = "identity", position = "dodge") + 
  labs(title = "Glucose Statistics",
       y = "Glucose Value",
       fill = "Group") + 
  theme_minimal()


sample_bmi98 <- quantile(sample_data$BMI, probs = 0.98)
population_bmi98 <- quantile(raw_data$BMI, probs = 0.98)


bmi_comparison <- data.frame(
  Group = c("Sample", "Population"),
  bmi98 = c(sample_bmi98, population_bmi98)
)

ggplot(bmi_comparison, aes(x = Group, y = bmi98, fill = Group)) + 
  geom_bar(stat = "identity") + 
  labs(title = "98th Percentile BMI Comparison",
       y = "BMI 98th Percentile",
       fill = "Group") + 
  theme_minimal()

bp_stat <- function(data) {
  mean_bp <- mean(data$BloodPressure)
  sd_bp <- sd(data$BloodPressure)
  percentile_95th_bp <- quantile(data$BloodPressure, probs = 0.95)
  return(c(mean_bp, sd_bp, percentile_95th_bp))
}

set.seed(123)

bootstrap_samples <- replicate(500, {
  sample_data <- raw_data %>% 
    sample_n(150, replace = TRUE)
  bp_stat(sample_data)
}, simplify = FALSE)

bootstrap_df <- as.data.frame(do.call(rbind, bootstrap_samples))

colnames(bootstrap_df) <- c("Mean", "StandardDeviation", "95thPercentile")

population_statistics <- bp_stat(raw_data)

comparison_data <- data.frame(
  Statistic = c("Mean", "Standard Deviation", "95th Percentile"),
  Sample = colMeans(bootstrap_df),
  Population = population_statistics
)

comparison_data_long <- comparison_data %>%
  pivot_longer(-Statistic, names_to = "Group", values_to = "Value")

ggplot(comparison_data_long, aes(x = Statistic, y = Value, fill = Group)) +
  geom_bar(stat = "identity", position = "dodge") +
  labs(title = "Comparison of Blood Pressure Statistics",
       y = "Value",
       fill = "Group") +
  theme_minimal()
