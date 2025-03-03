import { create } from 'zustand'

interface UserState {
  name: string
  gender: number
  birthDate: string
  birthTime: string
  lunarBirthDate: string
  age: number
  reportData: any  // 可以根据实际数据结构定义更具体的类型
  dailyFortune: any
  analysisResult: any
  analysisProgress: number
  setUserInfo: (info: Partial<UserState>) => void
  selectedTopic?: string;
  specialQuestion?: string;
}

export const useUserStore = create<UserState>((set) => ({
  name: '',
  gender: 1,
  birthDate: '',
  birthTime: '',
  lunarBirthDate: '',
  age: 0,
  reportData: null,
  dailyFortune: null,
  analysisResult: null,
  analysisProgress: 0,
  setUserInfo: (info) => set((state) => ({ ...state, ...info })),
  selectedTopic: '',
  specialQuestion: '',
})) 