import { wait } from "@/utils/wait";
// import { synthesizeVoiceApi } from "./synthesizeVoice"; // 不再需要这个旧接口
import { Viewer } from "../vrmViewer/viewer";
import { Screenplay } from "./messages";
import { Talk } from "./messages";

const createSpeakCharacter = () => {
  let lastTime = 0;
  let prevFetchPromise: Promise<unknown> = Promise.resolve();
  let prevSpeakPromise: Promise<unknown> = Promise.resolve();

  return (
    screenplay: Screenplay,
    viewer: Viewer,
    koeiroApiKey: string,
    onStart?: () => void,
    onComplete?: () => void
  ) => {
    const fetchPromise = prevFetchPromise.then(async () => {
      const now = Date.now();
      if (now - lastTime < 1000) {
        await wait(1000 - (now - lastTime));
      }

      // 这里调用下面的 fetchAudio
      const buffer = await fetchAudio(screenplay.talk, koeiroApiKey).catch(
        () => null
      );
      lastTime = Date.now();
      return buffer;
    });

    prevFetchPromise = fetchPromise;
    prevSpeakPromise = Promise.all([fetchPromise, prevSpeakPromise]).then(
      ([audioBuffer]) => {
        onStart?.();
        if (!audioBuffer) {
          return;
        }
        return viewer.model?.speak(audioBuffer, screenplay);
      }
    );
    prevSpeakPromise.then(() => {
      onComplete?.();
    });
  };
};

export const speakCharacter = createSpeakCharacter();

// --- 核心修改部分 ---

export const fetchAudio = async (
  talk: Talk,
  apiKey: string // 虽然不需要 Key 了，但为了保持参数兼容性，留着它
): Promise<ArrayBuffer> => {
  
  // 1. 准备你的 GPT-SoVITS 本地接口地址
  const apiBaseUrl = "http://127.0.0.1:9880/tts";

  // 2. 准备参数
  // 我们假设你已经在 api_v2.py 里设置好了 ref_audio_path 的默认值
  // 所以这里只需要传 text 和 text_lang
  const params = new URLSearchParams({
    text: talk.message,      // 要说的话
    text_lang: "zh",         // 强制中文
    prompt_lang: "zh"        // 提示语语言
  });

  // 如果你没在 api_v2.py 改默认值，你需要取消下面几行的注释，并填入你的路径：
  
  params.append("ref_audio_path", "D:\\workspace\\PartLawyer\\GPT-SoVITS\\鸣潮\\reference_audios\\randoms\\漂泊者_女\\中文\\zh_vo_zhuiyuejie_second_58_46_F.wav");
  params.append("prompt_text", "就像帕斯卡一直想要告诉你真相那样，就像你一直没有放弃为帕斯卡正名那样，你们的牵绊其实一直都在。");
  

  try {
    console.log("正在请求本地 TTS:", params.toString());
    
    // 3. 发送请求
    const res = await fetch(`${apiBaseUrl}?${params.toString()}`, {
      method: "GET",
    });

    if (!res.ok) {
      throw new Error(`GPT-SoVITS API Error: ${res.status} ${res.statusText}`);
    }

    // 4. 获取音频数据并返回
    const buffer = await res.arrayBuffer();
    return buffer;

  } catch (error) {
    console.error("TTS 生成失败:", error);
    throw error;
  }
};