hadoop jar ./target/q1a-1.0.jar edu.gatech.cse6242.Q1a /user/cse6242/test.tsv /user/cse6242/q1aoutputtest
hadoop fs -getmerge /user/cse6242/q1aoutputtest/ q1aoutputtest.tsv
hadoop fs -rm -r /user/cse6242/q1aoutputtest