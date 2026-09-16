import type { CapacitorConfig } from '@capacitor/cli'

const config: CapacitorConfig = {
  appId: 'cn.labourlawyer.mobile',
  appName: 'LabourLawyer 劳动仲裁助手',
  webDir: '../frontend/dist',
  server: {
    androidScheme: 'https',
    allowNavigation: ['127.0.0.1', 'localhost'],
  },
  android: {
    allowMixedContent: true,
    webContentsDebuggingEnabled: true,
  },
}

export default config
