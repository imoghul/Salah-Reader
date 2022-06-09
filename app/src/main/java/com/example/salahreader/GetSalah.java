package com.example.salahreader;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.List;
import java.util.Map;
import java.util.HashMap;

public class GetSalah {

    public static String getDataStr() {

        try {

            URL url = new URL("https://moneyless-gnu-7476.dataplicity.io/mtws-iqaamah-times/all");
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("GET");
            conn.setRequestProperty("Accept", "application/json");

            if (conn.getResponseCode() != 200) {
                throw new RuntimeException("Failed : HTTP error code : "
                                           + conn.getResponseCode());
            }

            BufferedReader br = new BufferedReader(new InputStreamReader(
                    (conn.getInputStream())));

            String output;

            while ((output = br.readLine()) != null) {
                conn.disconnect();
                return output;
            }

            conn.disconnect();
            return output;
        } catch (MalformedURLException e) {
            e.printStackTrace();
            return "Error";
        } catch (IOException e) {
            e.printStackTrace();
            return "Error";
        }

    }
    public static Map<String, String[]> parser(String times) {
        Map<String, String[]> res = new HashMap<String, String[]>();

        try {
            final JSONObject obj = new JSONObject(times);
            String[] days = {"Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"};

            for(int i = 0; i < days.length; ++i) {
                String[] timesDay = new String[5];
                JSONArray timesJson = obj.getJSONArray(days[i]);

                for(int t = 0; t < timesJson.length(); ++t) {
                    timesDay[t] = timesJson.getString(t);
                }

                res.put(days[i], timesDay);
            }

            return res;
        } catch (Exception e) {
            return res;
        }

    }
    //    public static void main(String[] args) {
    //	String[] days = {"Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"};
    //    	for (String entry:days){//for (Map.Entry<String, String[]> entry : parser(getDataStr()).entrySet()) {
    //  		System.out.println(entry);//.getKey());
    //		for(String i : parser(getDataStr()).get(entry)/*entry.getValue()*/) System.out.println(i);
    //	}
    //    }

}
