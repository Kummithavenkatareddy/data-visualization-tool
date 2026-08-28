# Sample Dataset & Example Workflows

This directory provides documentation on how to use the included sample dataset (`data/sample.csv`) with the Data Visualization Tool.

## Sample Dataset Overview

The sample dataset simulates sales performance metrics across categories, regions, and products:

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `Date` | String / Date | Transaction date (`YYYY-MM-DD`) |
| `Category` | Categorical | Product category (`Electronics`, `Furniture`, `Office Supplies`) |
| `Region` | Categorical | Sales region (`North`, `South`, `East`, `West`) |
| `Product` | Categorical | Product item name |
| `Sales` | Numeric | Sales revenue in USD |
| `Profit` | Numeric | Net profit in USD |
| `Units_Sold` | Numeric | Quantity of items sold |
| `Rating` | Numeric | Product rating score (1.0 - 5.0) |

---

## Example Visualization Workflows

### 1. Scatter Plot: Sales vs. Profit by Category
- **Chart Type**: `Scatter Plot`
- **X-Axis**: `Sales`
- **Y-Axis**: `Profit`
- **Color Column**: `Category`
- **Insight**: Explore correlation between sales amount and net profit across product categories.

---

### 2. Line Chart: Sales Trend Over Time
- **Chart Type**: `Line Chart`
- **X-Axis**: `Date`
- **Y-Axis**: `Sales`
- **Color Column**: `Region`
- **Insight**: Track sales trajectory across different regions over time.

---

### 3. Bar Chart: Total Sales by Category
- **Chart Type**: `Bar Chart`
- **X-Axis**: `Category`
- **Y-Axis**: `Sales`
- **Color Column**: `Region`
- **Insight**: Compare regional sales contributions across main product categories.

---

### 4. Histogram: Distribution of Units Sold
- **Chart Type**: `Histogram`
- **Numeric Column**: `Units_Sold`
- **Color Column**: `Category`
- **Insight**: Analyze the frequency distribution of order quantities per category.

---

### 5. Box Plot: Profit Margin Distribution by Region
- **Chart Type**: `Box Plot`
- **Numeric Column**: `Profit`
- **Category Column**: `Region`
- **Color Column**: `Region`
- **Insight**: Compare profit medians, quartiles, and outliers across geographical regions.

---

### 6. Pie Chart: Sales Breakdown by Category
- **Chart Type**: `Pie Chart`
- **Category Column**: `Category`
- **Values Column**: `Sales`
- **Insight**: Visualize the percentage breakdown of overall revenue by product category.
