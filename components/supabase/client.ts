// import { createClient } from '@supabase/supabase-js'
// import { ProxyAgent, setGlobalDispatcher } from 'undici'

// const dispatcher = new ProxyAgent({ uri: 'http://127.0.0.1:7890' });
// setGlobalDispatcher(dispatcher);
// export function createClient() {
//   return createBrowserClient(
//     process.env.NEXT_PUBLIC_SUPABASE_URL!,
//     process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
//   )
// }
// export const supabase = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL!, process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!)

import { createClient } from '@supabase/supabase-js';
// import { Database } from '@/types_chat';

// Define a function to create a Supabase client for client-side operations
export const supabase = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL!, process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!)
