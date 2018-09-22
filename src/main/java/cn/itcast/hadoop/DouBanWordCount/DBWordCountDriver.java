package cn.itcast.hadoop.DouBanWordCount;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class DBWordCountDriver {
    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
//        String[] otherArgs = new GenericOptionsParser(conf, args).getRemainingArgs();
//        if (otherArgs.length != 2) {
//            System.err.println("Usage: wordcount <in> <out>");
//            System.exit(2);
//        }
//        Job job = new Job(conf, "word count");
        Job job = Job.getInstance(conf);
        job.setJarByClass(DBWordCountDriver.class);
        job.setMapperClass(DBWordCountMapper.class);
        job.setReducerClass(DBWordCountReducer.class);

        //指定本次mr mapper阶段的输出 k  v的类型
        job.setMapOutputKeyClass(Text.class);
        job.setMapOutputValueClass(IntWritable.class);

        //指定本次mr 最终输出的k v的类型
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);

        FileInputFormat.setInputPaths(job, new Path("D:\\WebSpider\\talk.txt"));
        FileOutputFormat.setOutputPath(job, new Path("D:\\WebSpider\\xiaoshuo\\Noval\\output"));
        //提交，并且监控打印程序执行情况
        boolean b = job.waitForCompletion(true);
        System.exit(b?0:1);
    }
}
