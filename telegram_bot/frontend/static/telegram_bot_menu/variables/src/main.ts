import Toast from 'global_modules/toast';
import ClipboardJS from 'clipboard';

declare const successMessageTextForClipboard: string;
declare const errorMessageTextForClipboard: string;

const clipboard = new ClipboardJS('.btn-clipboard');
clipboard.on('success', (): void => new Toast(successMessageTextForClipboard, 'success').show());
clipboard.on('error', (): void => new Toast(errorMessageTextForClipboard, 'danger').show());