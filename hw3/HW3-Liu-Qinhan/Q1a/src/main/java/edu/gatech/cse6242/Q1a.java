package edu.gatech.cse6242;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.util.*;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import java.util.StringTokenizer;
import java.io.IOException;
import org.apache.hadoop.mapreduce.Mapper.Context;
import java.io.StringReader;
import org.apache.hadoop.mapreduce.lib.input.KeyValueTextInputFormat;
import java.lang.System;

public class Q1a {

  public static class WordMapper extends Mapper<Text, Text, Text, Text>{
        private Text weight = new Text();
        public void map(Text key, Text value, Context context) throws IOException, InterruptedException{
            StringTokenizer itr = new StringTokenizer(value.toString(),"\t");
            String word = new String();
            while (itr.hasMoreTokens())
            {
                word = itr.nextToken();
            }
            weight.set(word);
            context.write(key, weight);

        }
    }
    public static class FindMaxReducer
    extends Reducer<Text, Text, Text, Text>{
        private Text result = new Text();
        public void reduce(Text key, Iterable<Text> values, Context context)
          throws IOException, InterruptedException{
            String weight = "";
            int max = 0;
            for (Text val : values){
                int var = Integer.parseInt((val.toString()));
                if (var > max) {
                  max = var;
                }
            }
            if (max != 0) {
              weight += max;
              result.set(weight);
              context.write(key, result);
            }
        }
    }

  public static void main(String[] args) throws Exception {
    Configuration conf = new Configuration();
    Job job = Job.getInstance(conf, "Q1a");

    /* TO DO: Needs to be implemented */

    job.setJarByClass(Q1a.class);
    job.setMapperClass(WordMapper.class);
    job.setReducerClass(FindMaxReducer.class);
    job.setOutputKeyClass(Text.class);
    job.setOutputValueClass(Text.class);
    job.setInputFormatClass(KeyValueTextInputFormat.class);

    FileInputFormat.addInputPath(job, new Path(args[0]));
    FileOutputFormat.setOutputPath(job, new Path(args[1]));
    System.exit(job.waitForCompletion(true) ? 0 : 1);
  }
}
