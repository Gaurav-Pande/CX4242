package edu.gatech.cse6242

import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.SparkConf
import org.apache.spark.sql.SQLContext
import org.apache.spark.sql.functions._
import org.apache.spark.sql.functions.udf

object Q2 {
    case class Graph1(src1: Int, tar1: Int, weight1: Double)
    case class Graph2(src2: Int, tar2: Int, weight2: Double)

    def main(args: Array[String]) {
        val sc = new SparkContext(new SparkConf().setAppName("Q2"))
        val sqlContext = new SQLContext(sc)
        import sqlContext.implicits._

        // Read the file
        val file = sc.textFile("hdfs://localhost:8020" + args(0))
        /* TODO: Needs to be implemented */

        val a=file.map(_.split("\t"))
            .map(e=>Graph1(e(0).trim.toInt,e(1).trim.toInt, e(2).trim.toDouble)).toDF()

        val b=file.map(_.split("\t"))
            .map(e=>Graph2(e(0).trim.toInt,e(1).trim.toInt, e(2).trim.toDouble)).toDF()

        val a1=a.filter("weight1 >= 10").groupBy("src1")
        val b1=b.filter("weight2 >= 10").groupBy("tar2")

        val a2=a1.agg(avg($"weight1"))
        val b2=b1.agg(avg($"weight2"))

        val df0 = a2.join(b2, a2("src1") === b2("tar2"), "outer")

        // Replace all null values with 0.0
        val df1 = df0.na.fill(0.0, Seq("avg(weight1)")).na.fill(0.0, Seq("avg(weight2)"))

        // Fill in the empty fields
        val df2 = df1.withColumn("src1", when( col("src1").isNull, col("tar2")).otherwise(col("src1")) )
                     .withColumn("tar2", when( col("tar2").isNull, col("src1")).otherwise(col("tar2")) )

        val subFunc : (Double,Double)=>Double=(num1:Double,num2:Double)=>{num1-num2}

        // The UDF for substracting 2 columns
        val subUDF = udf(subFunc)

        // Add a new "sub" column
        val df = df2.withColumn("sub",subUDF(df2.col("avg(weight1)"),df2.col("avg(weight2)")))

        var out = df.select(df("src1"), df("sub"))
        // out.show()
        // df.show()
        // store output on given HDFS path.
        out.rdd.map(_.mkString("\t").replace("[","").replace("]", "")).saveAsTextFile("hdfs://localhost:8020" + args(1))
    }
}
