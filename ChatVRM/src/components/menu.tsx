import { IconButton } from "./iconButton";
import { Message } from "@/features/messages/messages";
import { KoeiroParam } from "@/features/constants/koeiroParam";
import { ChatLog } from "./chatLog";
import React, { useCallback, useContext, useRef, useState } from "react";
// import { Settings } from "./settings"; 
import { ViewerContext } from "@/features/vrmViewer/viewerContext";
import { AssistantText } from "./assistantText";

type Props = {
  openAiKey: string;
  systemPrompt: string;
  chatLog: Message[];
  koeiroParam: KoeiroParam;
  assistantMessage: string;
  koeiromapKey: string;
  onChangeSystemPrompt: (systemPrompt: string) => void;
  onChangeAiKey: (key: string) => void;
  onChangeChatLog: (index: number, text: string) => void;
  onChangeKoeiromapParam: (param: KoeiroParam) => void;
  handleClickResetChatLog: () => void;
  handleClickResetSystemPrompt: () => void;
  onChangeKoeiromapKey: (key: string) => void;
};

export const Menu = ({
  openAiKey,
  systemPrompt,
  chatLog,
  koeiroParam,
  assistantMessage,
  koeiromapKey,
  onChangeSystemPrompt,
  onChangeAiKey,
  onChangeChatLog,
  onChangeKoeiromapParam,
  handleClickResetChatLog,
  handleClickResetSystemPrompt,
  onChangeKoeiromapKey,
}: Props) => {
  // const [showSettings, setShowSettings] = useState(false); 
  const [showChatLog, setShowChatLog] = useState(false);
  const { viewer } = useContext(ViewerContext);
  
  // --- 设置相关逻辑已注释 ---

  return (
    <>
      <div className="absolute z-10 m-24">
        <div className="grid grid-flow-col gap-[8px]">
          
          {/* 设置按钮已注释 */}
          {/* <IconButton
            iconName="24/Menu"
            label="设置" 
            isProcessing={false}
            onClick={() => setShowSettings(true)}
          ></IconButton> 
          */}

          {/* ==================================================== */}
          {/* 新增：清空记录按钮 */}
          {/* iconName 对应 public/icons/24/Trash.svg，如果没有该文件，图标会空白 */}
          {/* 你可以去下载一个 svg 命名为 Trash.svg 放入对应目录 */}
          {/* ==================================================== */}
          <IconButton
            iconName="24/Trash" 
            label="清空"
            isProcessing={false}
            disabled={chatLog.length <= 0} // 如果没有记录则禁用
            onClick={() => {
                if (window.confirm("确定要清空所有对话记录吗？此操作不可恢复。")) {
                    handleClickResetChatLog();
                }
            }}
          />

          {/* 对话记录显隐按钮 */}
          {showChatLog ? (
            <IconButton
              iconName="24/CommentOutline"
              label="对话记录"
              isProcessing={false}
              onClick={() => setShowChatLog(false)}
            />
          ) : (
            <IconButton
              iconName="24/CommentFill"
              label="对话记录"
              isProcessing={false}
              disabled={chatLog.length <= 0}
              onClick={() => setShowChatLog(true)}
            />
          )}
        </div>
      </div>

      {/* 对话记录弹窗 */}
      {showChatLog && <ChatLog messages={chatLog} />}

      {/* 设置弹窗已注释 */}
      {/* {showSettings && ( ... )} */}

      {/* 助手消息气泡 (当不看聊天记录时显示) */}
      {!showChatLog && assistantMessage && (
        <AssistantText message={assistantMessage} />
      )}
    </>
  );
};