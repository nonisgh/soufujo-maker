-- 送付状メーカー：クラウド同期（Supabase SQL Editor で1回だけ実行）
-- 既存の password_config には触れません。テーブルを1つ足すだけです。
--
-- しくみ
--   * ログインは Supabase Auth（メールアドレス＋パスワード）。ユーザーはダッシュボードで作成済みのものを使う
--   * 1人1行。中身（今の設定・保存したフォーマット・差出人・本文）は data(jsonb) にまとめて入れる
--   * RLS で「ログインした本人の行だけ」読み書きできる。公開キーだけでは誰の行も読めない
--   * Realtime で、ほかの端末の変更をすぐ受け取る（RLS が効くので本人の行の変更だけ届く）

create table if not exists public.soufu_state (
  user_id    uuid primary key default auth.uid() references auth.users(id) on delete cascade,
  data       jsonb not null default '{}'::jsonb,
  updated_at timestamptz not null default now()
);

alter table public.soufu_state enable row level security;

drop policy if exists "soufu_state select own" on public.soufu_state;
drop policy if exists "soufu_state insert own" on public.soufu_state;
drop policy if exists "soufu_state update own" on public.soufu_state;
drop policy if exists "soufu_state delete own" on public.soufu_state;
create policy "soufu_state select own" on public.soufu_state for select to authenticated using (user_id = auth.uid());
create policy "soufu_state insert own" on public.soufu_state for insert to authenticated with check (user_id = auth.uid());
create policy "soufu_state update own" on public.soufu_state for update to authenticated using (user_id = auth.uid()) with check (user_id = auth.uid());
create policy "soufu_state delete own" on public.soufu_state for delete to authenticated using (user_id = auth.uid());

revoke all on public.soufu_state from anon;
grant select, insert, update, delete on public.soufu_state to authenticated;

-- リアルタイム同期のため、変更を配信する対象に入れる（すでに入っていればエラーになるので、そのときはこの行は無視してOK）
alter publication supabase_realtime add table public.soufu_state;
