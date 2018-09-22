package cn.itcast.hadoop.DouBanWordCount;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

import java.io.IOException;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class DBWordCountReducer extends Reducer<Text,IntWritable,Text,IntWritable> {
    private IntWritable v = new IntWritable();

    public void reduce(Text key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException {
        int sum = 0;
        String keys;
        for (IntWritable value : values) {
            keys = key.toString();
            String regex = "[\\u4e00-\\u9fa5]";
            Pattern pattern = Pattern.compile(regex);
            Matcher matcher = pattern.matcher(keys);
            int count=0;
            while (matcher.find()) {
                count++;
            }
            if(count <= 1){
                continue;
            }
            sum += value.get();
        }
        v.set(sum);
        context.write(key, v);
    }
}
