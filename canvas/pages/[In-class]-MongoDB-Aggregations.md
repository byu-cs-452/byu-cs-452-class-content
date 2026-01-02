### MongoDB Aggregations

In MongoDB, **aggregations** are operations used to process and transform data in a collection. They allow you to calculate aggregated results, such as counts, sums, averages, or more complex analyses, from your dataset. Aggregation operations process data records and return computed results, enabling you to analyze data and extract meaningful insights.

The **aggregation pipeline** is a framework for data aggregation modeled as a sequence of stages. Each stage transforms the data and passes it to the next stage. The most common stages include:

* **`$match`**: Filters data to pass only those documents that match the specified condition.
* **`$group`**: Groups documents by a specified key and performs aggregation operations, like summing or averaging.
* **`$sort`**: Sorts documents by a specified field.
* **`$project`**: Reshapes each document by specifying fields to include or exclude, or by adding computed fields.
* **`$limit`**: Limits the number of documents.
* **`$skip`**: Skips a specified number of documents.
* **`$unwind`**: Deconstructs an array field from a document into multiple documents.

#### Example:

```
db.sales.aggregate([  
  { $match: { status: "A" } },  
  { $group: { _id: "$item", total: { $sum: "$amount" } } },  
  { $sort: { total: -1 } }  
])
```

### Materials

**Slides:** Please review [these slides](../files/MoreMongoDB-1.pptx "Link") prior to class

**Starter code:**[Click here](https://colab.research.google.com/github/byu-cs-452/byu-cs-452-class-content/blob/main/mongo/mongodb_inclass_aggregations_starter_code.ipynb) to open the colab notebook

**Solution:** [Click here](https://colab.research.google.com/drive/1Zrko5BHU_Z-jAx5_WPkwO3onOC-pa6f1?usp=sharing "Link") to open the colab notebook