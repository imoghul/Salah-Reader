package com.example.salahreader;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;

public class DailyRefresh extends BroadcastReceiver {
    @Override
    public void onReceive(Context context, Intent intent) {
        SettingsActivity.sf.updateTimes();
    }
}