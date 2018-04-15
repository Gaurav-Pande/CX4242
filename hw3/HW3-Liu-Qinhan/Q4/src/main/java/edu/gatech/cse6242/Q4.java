package edu.gatech.cse6242;

import java.io.IOException;
import java.util.StringTokenizer;
import java.lang.Object;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.Configuration;

import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.util.*;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import java.io.IOException;

public class Q4 {

  public static class DifferenceMapper extends Mapper<Object, Text, IntWritable, IntWritable>
  {
      private IntWritable src = new IntWritable();
      private IntWritable tar = new IntWritable();
      public void map(Object key, Text value, Context context) throws IOException, InterruptedException
      {
          StringTokenizer itr = new StringTokenizer(value.toString(), "\n");
          while (itr.hasMoreTokens()) {
            String[] s = itr.nextToken().split("\t");
            src.set(Integer.parseInt(s[0]));
            tar.set(Integer.parseInt(s[1]));
            context.write(src, new IntWritable(-1));
            context.write(tar, new IntWritable(1));
          }
      }
  }

  public static class DifferenceReducer extends Reducer<IntWritable, IntWritable, IntWritable, IntWritable>
  {
      private IntWritable diff = new IntWritable();
      public void reduce(IntWritable key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException
      {
          int sum = 0;
          for (IntWritable val : values)
          {
              sum += val.get();
          }
          diff.set(sum);
          context.write(key, diff);
      }
  }

  public static class CountMapper
    extends Mapper<Object, Text, IntWritable, IntWritable>{

    private final static IntWritable one = new IntWritable(1);
    private IntWritable node = new IntWritable();

    public void map(Object key, Text value, Context context
                    ) throws IOException, InterruptedException {
      StringTokenizer itr = new StringTokenizer(value.toString(), "\n");
      while (itr.hasMoreTokens()) {
        String line = itr.nextToken();
        String pair[] = line.split("\t");

        node.set(Integer.parseInt(pair[1]));
        context.write(node, one);
      }
    }
  }

  public static class CountReducer
       extends Reducer<IntWritable,IntWritable,IntWritable,IntWritable> {
    private IntWritable result = new IntWritable();

    public void reduce(IntWritable key, Iterable<IntWritable> values,
                       Context context
                       ) throws IOException, InterruptedException {
      int sum = 0;
      for (IntWritable val : values) {
        sum += val.get();
      }
      result.set(sum);
      context.write(key, result);
    }
  }

  public static void main(String[] args) throws Exception {
    Configuration conf = new Configuration();
    Job job = Job.getInstance(conf, "job1");

    job.setJarByClass(Q4.class);
    job.setMapperClass(DifferenceMapper.class);
    job.setReducerClass(DifferenceReducer.class);
    job.setOutputKeyClass(IntWritable.class);
    job.setOutputValueClass(IntWritable.class);

    FileInputFormat.addInputPath(job, new Path(args[0]));
    FileOutputFormat.setOutputPath(job, new Path("pre_out"));

    job.waitForCompletion(true);

    Job job2 = Job.getInstance(conf, "job2");

    job2.setJarByClass(Q4.class);
    job2.setMapperClass(CountMapper.class);
    job2.setReducerClass(CountReducer.class);
    job2.setOutputKeyClass(IntWritable.class);
    job2.setOutputValueClass(IntWritable.class);

    FileInputFormat.addInputPath(job2, new Path("pre_out"));
    FileOutputFormat.setOutputPath(job2, new Path(args[1]));
    System.exit(job2.waitForCompletion(true) ? 0 : 1);
  }
}
