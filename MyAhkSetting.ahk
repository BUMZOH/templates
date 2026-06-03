#NoEnv
#UseHook
#InstallKeybdHook

SendMode Input
SetWorkingDir %A_ScriptDir%

; --------------------------------------
; 無変換 + hjkl = 矢印
; --------------------------------------

vk1D & h::Send,{Blind}{Left}
vk1D & j::Send,{Blind}{Down}
vk1D & k::Send,{Blind}{Up}
vk1D & l::Send,{Blind}{Right}

; --------------------------------------
; Home / End / PgUp / PgDn
; --------------------------------------

vk1D & u::Send,{Blind}{Home}
vk1D & m::Send,{Blind}{End}

vk1D & i::Send,{Blind}{PgUp}
vk1D & ,::Send,{Blind}{PgDn}

; --------------------------------------
; Delete / Backspace
; --------------------------------------

vk1D & n::Send,{Blind}{Del}
vk1D & y::Send,{Blind}{BS}

