package cn.itcast.hadoop.DouBanWordCount.DBsort;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

import java.io.IOException;

public class DBSortDriver {
    public static class DBSortMapper extends Mapper<LongWritable, Text,LongWritable , Text> {
        LongWritable k= new LongWritable();
        Text v = new Text();
        @Override
        protected void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
            String line = value.toString();

            String[] fields = line.split("\t");

            String word = fields[0];

            long sum = Long.parseLong(fields[1]);

            k.set(sum);
            v.set(word);
            context.write(k,v);
        }
    }

    public static class DBSortReducer extends Reducer<LongWritable,Text,Text,LongWritable> {
        @Override
        protected void reduce(LongWritable key, Iterable<Text> values, Context context) throws IOException, InterruptedException {
            /**
             * (1) 使用方法iterator()要求容器返回一个Iterator。第一次调用Iterator的next()方法时，它返回序列的第一个元素。注意：iterator()方法是java.lang.Iterable接口,被Collection继承。
             * (2) 使用next()获得序列中的下一个元素。
             */
            context.write(values.iterator().next(),key);
        }
    }

    public static void main(String[] args) throws Exception {
        //通过Job来封装本次mr的相关信息
        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf);

        //指定本次mr job  jar包运行的主类
        job.setJarByClass(DBSortDriver.class);

        //指定本次mr 所用的mapper  reducer类分别是什么
        job.setMapperClass(DBSortMapper.class);
        job.setReducerClass(DBSortReducer.class);

        //指定本次mr mapper阶段的输出 k  v的类型
        job.setMapOutputKeyClass(LongWritable.class);
        job.setMapOutputValueClass(Text.class);

        //指定本次mr 最终输出的k v的类型
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(LongWritable.class);

        //指定本次mr 输入的数据路径 和最终输出结果存放在什么位置
//        FileInputFormat.setInputPaths(job,"/wordcount/output/");
//        FileOutputFormat.setOutputPath(job,new Path("/wordcount/outputsort"));

//        这是本地运行时的路径，精确到文件名
        FileInputFormat.setInputPaths(job, new Path("D:\\WebSpider\\xiaoshuo\\Noval\\output\\part-r-00000"));
        FileOutputFormat.setOutputPath(job, new Path("D:\\WebSpider\\xiaoshuo\\Noval\\output\\outputsort"));

        //提交程序
        //job.submit();
        //提交，并且监控打印程序执行情况
        boolean b = job.waitForCompletion(true);
        System.exit(b ? 0 : 1);
    }
}


