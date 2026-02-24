import { wait } from "@/utils/wait";
import { Viewer } from "../vrmViewer/viewer";
import { Screenplay } from "./messages";
import { Talk } from "./messages";

// === 新增：全局语音打断信号 Token ===
let currentSpeakToken = 0;

export const interruptSpeakCharacter = () => {
  currentSpeakToken++; // 每次调用改变 Token，旧队列的语音就会失效作废
  console.log("🛑 收到新问题，已清空并打断之前的语音队列！");
};

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
    // 记录这句台词进入队列时的身份 Token
    const myToken = currentSpeakToken;

    const fetchPromise = prevFetchPromise.then(async () => {
      // 核心打断逻辑：如果 Token 过期（用户问了新问题），直接抛弃这句台词
      if (myToken !== currentSpeakToken) return null;

      const now = Date.now();
      if (now - lastTime < 1000) {
        await wait(1000 - (now - lastTime));
      }

      if (myToken !== currentSpeakToken) return null;

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
        // 播放前做最后一次检查，如果被打断则保持沉默
        if (myToken !== currentSpeakToken || !audioBuffer) {
          onComplete?.();
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

export const fetchAudio = async (
  talk: Talk,
  apiKey: string
): Promise<ArrayBuffer> => {
  const apiBaseUrl = "http://127.0.0.1:9880/tts";

  // === 核心修复 1：在正则屏蔽列表里加入了 \- ，彻底消灭“减”字发音 ===
  const cleanText = talk.message
    .replace(/<think>[\s\S]*?<\/think>\n*/gi, "") 
    .replace(/<think>[\s\S]*/gi, "")              
    .replace(/<[^>]+>/g, "")                      
    .replace(/[\*\#\>\`\-]/g, "") // <--- 这里加入了 \-
    .replace(/\[(.*?)\]\(.*?\)/g, "$1")           
    .replace(/[\n\r]+/g, "，")                    
    .trim();

  if (!cleanText) {
    throw new Error("Empty text after cleaning");
  }

  const params = new URLSearchParams();
  params.append("text", cleanText);        
  params.append("text_lang", "zh");        
  params.append("prompt_lang", "zh");      

  params.append("ref_audio_path", "D:/Desktop/MingChao/reference_audios/randoms/漂泊者_女/中文/zh_vo_zhuiyuejie_second_58_46_F.wav");
  params.append("prompt_text", "就像帕斯卡一直想要告诉你真相那样，就像你一直没有放弃为帕斯卡正名那样，你们的牵绊其实一直都在。");

  try {
    const res = await fetch(`${apiBaseUrl}?${params.toString()}`, {
      method: "GET",
    });
    if (!res.ok) {
      const errorText = await res.text().catch(() => "Unknown error");
      throw new Error(`GPT-SoVITS API Error: ${res.status} - ${errorText}`);
    }
    return await res.arrayBuffer();
  } catch (error) {
    console.error("TTS 生成失败:", error);
    throw error;
  }
};