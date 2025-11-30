import React, { useCallback } from 'react';
import { UploadCloud } from 'lucide-react';

interface FileUploadProps {
    onUpload: (file: File) => void;
    isUploading: boolean;
}

export const FileUpload: React.FC<FileUploadProps> = ({ onUpload, isUploading }) => {
    const handleDrop = useCallback(
        (e: React.DragEvent<HTMLDivElement>) => {
            e.preventDefault();
            if (e.dataTransfer.files && e.dataTransfer.files[0]) {
                onUpload(e.dataTransfer.files[0]);
            }
        },
        [onUpload]
    );

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            onUpload(e.target.files[0]);
        }
    };

    return (
        <div
            className="w-full max-w-2xl mx-auto mt-10 p-8 border-2 border-dashed border-indigo-300 rounded-2xl bg-indigo-50 hover:bg-indigo-100 transition-colors cursor-pointer flex flex-col items-center justify-center text-center"
            onDrop={handleDrop}
            onDragOver={(e) => e.preventDefault()}
        >
            <input
                type="file"
                id="file-upload"
                className="hidden"
                onChange={handleChange}
                accept=".csv,.xlsx,.xls"
                disabled={isUploading}
            />
            <label htmlFor="file-upload" className="cursor-pointer w-full h-full flex flex-col items-center">
                <div className="p-4 bg-white rounded-full shadow-md mb-4">
                    <UploadCloud className="w-10 h-10 text-indigo-600" />
                </div>
                <h3 className="text-xl font-semibold text-gray-800 mb-2">
                    {isUploading ? 'Uploading...' : 'Upload your dataset'}
                </h3>
                <p className="text-gray-500 mb-6">Drag & drop or click to browse (CSV, Excel)</p>
                <span className="px-6 py-2 bg-indigo-600 text-white rounded-lg font-medium shadow-lg hover:bg-indigo-700 transition-all">
                    Select File
                </span>
            </label>
        </div>
    );
};
