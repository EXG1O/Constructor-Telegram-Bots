import { Toast } from 'global_modules/toast';
import ClipboardJS from 'clipboard';

declare const successMessageTextForClipboard: string;
declare const errorMessageTextForClipboard: string;

const clipboard = new ClipboardJS('.btn-clipboard');
clipboard.on('success', () => new Toast(successMessageTextForClipboard, 'success').show());
clipboard.on('error', () => new Toast(errorMessageTextForClipboard, 'danger').show());