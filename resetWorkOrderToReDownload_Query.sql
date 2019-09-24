/****** Script for SelectTopNRows command from SSMS  ******/
SELECT TOP (1000) [RefId]
      ,[HostName]
      ,[RemoteFolder]
      ,[FileName]
      ,[DateDetected]
      ,[DownloadStatus]
      ,[DateDownloaded]
      ,[ErrorMessage]
      ,[DownloaderId]
      ,[DateAllocated]
      ,[RetryCounter]
  FROM [WMS_CHVDP].[dbo].[CHVDP_FTP_Files]
  where FileName in('22588828.pdf','13896883.pdf')
  order by DateDetected desc
  
  --reset files to allow downloading once again.

UPDATE [dbo].[CHVDP_FTP_Files]
   SET [DownloadStatus] = 'NEW'
      ,[DateDownloaded] = NULL
      ,[ErrorMessage] = NULL
      ,[DownloaderId] = NULL
      ,[DateAllocated] = NULL
      ,[RetryCounter] = NULL
 where FileName in('22588828.pdf','13896883.pdf')
GO

