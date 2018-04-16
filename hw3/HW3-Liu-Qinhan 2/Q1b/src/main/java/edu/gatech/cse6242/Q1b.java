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
import java.io.DataInput;
import java.io.DataOutput;
import java.lang.Math;

class CompositeKeyWritable implements Writable,WritableComparable<CompositeKeyWritable> {

	private String depthNum;
	private String compPair;
	private String compPair2;

	public CompositeKeyWritable() {}

	public CompositeKeyWritable(String depthNum, String compPair, String compPair2) {
		this.depthNum = depthNum;
		this.compPair = compPair;
		this.compPair2 = compPair2;
	}

	public void readFields(DataInput dataInput) throws IOException {
		depthNum = WritableUtils.readString(dataInput);
		compPair = WritableUtils.readString(dataInput);
		compPair2 = WritableUtils.readString(dataInput);
	}

	public void write(DataOutput dataOutput) throws IOException {
		WritableUtils.writeString(dataOutput, depthNum);
		WritableUtils.writeString(dataOutput, compPair);
		WritableUtils.writeString(dataOutput, compPair2);
	}

	public int compareTo(CompositeKeyWritable keyPair) {
		int diff =	Math.abs( Integer.parseInt(compPair) - Integer.parseInt(keyPair.compPair) ) +
					Math.abs( Integer.parseInt(keyPair.compPair2) - Integer.parseInt(compPair2) ) +
					Math.abs( Integer.parseInt(depthNum) - Integer.parseInt(keyPair.depthNum) );
		return diff;
	}

	public String getDepthNum() {
		return depthNum;
	}

	public void setDepthNum(String depthNum) {
		this.depthNum = depthNum;
	}

	public String getCompPair() {
		return compPair;
	}

	public void setCompPair(String compPair) {
		this.compPair = compPair;
	}

	public String getCompPair2() {
		return compPair2;
	}

	public void setCompPair2(String compPair2) {
		this.compPair2 = compPair2;
	}
}

class SecSortBasicPartitioner extends Partitioner<CompositeKeyWritable, NullWritable> {

	public int getPartition(CompositeKeyWritable key, NullWritable value,int numReduceTasks) {
		return (key.getCompPair().hashCode() % numReduceTasks);
	}
}

class SecSortBasicCompKeySortComparator extends WritableComparator {

	protected SecSortBasicCompKeySortComparator() {
		super(CompositeKeyWritable.class, true);
	}

	public int compare(WritableComparable w1, WritableComparable w2) {
		CompositeKeyWritable key1 = (CompositeKeyWritable) w1;
		CompositeKeyWritable key2 = (CompositeKeyWritable) w2;

		// int diff =	Math.abs( Integer.parseInt(key1.getCompPair()) - Integer.parseInt(key2.getCompPair()) ) +
		// 			Math.abs( Integer.parseInt(key2.getCompPair2()) - Integer.parseInt(key1.getCompPair2()) ) +
		// 			Math.abs( Integer.parseInt(key1.getDepthNum()) - Integer.parseInt(key2.getDepthNum()) );
		// return diff;

		int diff = Integer.parseInt(key1.getCompPair()) - Integer.parseInt(key2.getCompPair());
		if (diff == 0) {
			diff = Integer.parseInt(key2.getCompPair2()) - Integer.parseInt(key1.getCompPair2());
			if (diff == 0) {
					diff = Integer.parseInt(key1.getDepthNum()) - Integer.parseInt(key2.getDepthNum());
				}
		}
		return diff;
	}
}

class SecSortBasicGroupingComparator extends WritableComparator {
	protected SecSortBasicGroupingComparator() {
		super(CompositeKeyWritable.class, true);
	}

	public int compare(WritableComparable w1, WritableComparable w2) {
		CompositeKeyWritable key1 = (CompositeKeyWritable) w1;
		CompositeKeyWritable key2 = (CompositeKeyWritable) w2;
		return key1.getCompPair().compareTo(key2.getCompPair());
	}
}

public class Q1b {

	public static class SecSortBasicMapper extends
		Mapper<LongWritable, Text, CompositeKeyWritable, NullWritable> {

		public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
			if (value.toString().length() > 0) {
				String attr[] = value.toString().split("\t");
				context.write( new CompositeKeyWritable(attr[0].toString(),attr[1].toString(),attr[2].toString()), NullWritable.get());
			}
		}
	}

	public static class SecSortBasicReducer extends Reducer<CompositeKeyWritable, NullWritable, String, String> {

	public void reduce(CompositeKeyWritable key, Iterable<NullWritable> values, Context context)
		throws IOException, InterruptedException {
		context.write(key.getCompPair(), key.getDepthNum());
	}
}

	public static void main(String[] args) throws Exception {
		Configuration conf = new Configuration();
		Job job = Job.getInstance(conf, "Q1b");

		/* TO DO: Needs to be implemented */
		job.setJarByClass(Q1b.class);

		job.setMapperClass(SecSortBasicMapper.class);
		job.setMapOutputKeyClass(CompositeKeyWritable.class);
		job.setMapOutputValueClass(NullWritable.class);
		job.setPartitionerClass(SecSortBasicPartitioner.class);
		job.setSortComparatorClass(SecSortBasicCompKeySortComparator.class);
		job.setGroupingComparatorClass(SecSortBasicGroupingComparator.class);
		job.setReducerClass(SecSortBasicReducer.class);
		job.setOutputKeyClass(CompositeKeyWritable.class);
		job.setOutputValueClass(NullWritable.class);

		FileInputFormat.addInputPath(job, new Path(args[0]));
		FileOutputFormat.setOutputPath(job, new Path(args[1]));
		System.exit(job.waitForCompletion(true) ? 0 : 1);
	}
}
